#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Download an artifact from a different Gitlab project
"""

# included batteries
from datetime import datetime, timezone
import os
import sys
import urllib.parse

# 3rd-party
import dotenv  # pip install python-dotenv
import requests  # pip install requests

DEFAULT_API_BASE_URL = 'https://gitlab.com/api/v4'
DEFAULT_BRANCH = 'main'
DEFAULT_CA_PATH = '/etc/ssl/certs/ca-certificates.crt'
DEFAULT_PROJECT_ID = 'graphviz/graphviz'
DEFAULT_JOB_NAME = 'portable-source'
DEFAULT_DL_PATH = 'artifact.zip'

DEFAULT_CONFIG = {
    'GLDL_API_BASE_URL': DEFAULT_API_BASE_URL,
    'GLDL_BRANCH': DEFAULT_BRANCH,
    'GLDL_CA_PATH': DEFAULT_CA_PATH,
    'GLDL_PROJECT_ID': DEFAULT_PROJECT_ID,
    'GLDL_TOKEN': None,
    'GLDL_JOB_NAME': DEFAULT_JOB_NAME,
    'GLDL_DL_PATH': DEFAULT_DL_PATH,
}


class GitlabError(Exception):
    """Gitlab REST error"""


class GitlabApi:
    """Handle REST calls to the Gitlab API"""
    def __init__(
        self,
        ca_path=DEFAULT_CA_PATH,
        base_url=DEFAULT_API_BASE_URL,
        project_id=DEFAULT_PROJECT_ID,
        token=None,
    ):
        self.branch = DEFAULT_BRANCH
        self.base_url = base_url
        self.project_id = urllib.parse.quote_plus(project_id)
        self.verify = ca_path
        self.session = requests.session()
        self.session.headers.update({'PRIVATE-TOKEN': token})

    def get_pipeline_id(self, branch=None):
        """Get the latest pipeline-id of a given branch"""
        if branch is None:
            branch = self.branch
        pipelines_url = f'{self.base_url}/projects/{self.project_id}/pipelines'
        params = {
            'order_by': 'updated_at',
            'ref': branch,
            'scope': 'finished',
            'sort': 'desc',
            'status': 'success',
            'per_page': 1,
        }
        try:
            response = self.session.get(
                pipelines_url,
                params=params,
                verify=self.verify,
                timeout=(9.05, 30.05),
            )
        except requests.exceptions.ConnectTimeout as err:
            raise GitlabError('Connection timed out. Check route!') from err
        content = response.json()
        if response.status_code == 401:
            print(f"Content: {content}")
            raise GitlabError('Bad authorization. Check token!')
        if response.status_code == 404:
            print(f"Content: {content}")
            print(f"Project ID: {self.project_id}")
            raise GitlabError('Project not found')
        if response.status_code != 200:
            print(f"Message: {content}")
            raise GitlabError(f'Request failed with {response.status_code}')
        for pipeline in response.json():
            if pipeline['status'] == 'success':
                return pipeline['id']
        raise GitlabError('No successful pipeline found')

    def get_job_id(self, pipeline_id, job_name='build-job'):
        """Get a job-id by job-name of a given pipeline-id"""
        job_name = urllib.parse.quote_plus(job_name)
        jobs_url = (
            f'{self.base_url}/projects/{self.project_id}'
            f'/pipelines/{pipeline_id}/jobs'
        )
        params = {'scope': 'success', 'per_page': 100}
        response = self.session.get(jobs_url, params=params)
        if response.status_code != 200:
            raise GitlabError(f'Request failed with {response.status_code}')
        jobs = response.json()
        if not jobs:
            raise GitlabError('No jobs found')
        for job in jobs:
            if job['name'] == job_name:
                return job['id']
        raise GitlabError('No job matched')

    def ensure_archive_availability(self, job_id):
        """Test if the current job has a downloadable archive"""
        job_url = f'{self.base_url}/projects/{self.project_id}/jobs/{job_id}'
        response = self.session.get(job_url)
        if response.status_code != 200:
            raise GitlabError(f'Request failed with {response.status_code}')
        job = response.json()
        if 'artifacts_file' not in job or 'artifacts_expire_at' not in job:
            raise GitlabError('archive not found')
        try:
            artifacts_expire_at = datetime.strptime(
                job["artifacts_expire_at"],
                '%Y-%m-%dT%H:%M:%S.%f%z',
            )
        except ValueError as err:
            print(f'Failed to parse artifacts_expire_at: {err}')
        else:
            time_left = artifacts_expire_at - datetime.utcnow().replace(
                tzinfo=timezone.utc
            )
            seconds_left = time_left.total_seconds()
            if seconds_left < 0:
                raise GitlabError('artifacts expired')
        return

    def download_artifact(self, job_id, download_path):
        """Download the artifact zip-file of a given job"""
        artifacts_url = (
            f'{self.base_url}/projects/{self.project_id}'
            f'/jobs/{job_id}/artifacts'
        )
        # Hosted on `de-2.s3.psmanaged.com`
        with self.session.get(artifacts_url, stream=True) as response:
            if response.status_code != 200:
                raise GitlabError(
                    f'Request failed with {response.status_code}'
                )
            with open(download_path, 'wb') as buffered_writer:
                for chunk in response.iter_content(chunk_size=8192):
                    buffered_writer.write(chunk)
        return


def get_config(default_config):
    """Read config from .env file and override with env-vars"""
    config = default_config.copy()
    for key, value in dotenv.dotenv_values().items():
        if key in default_config:
            config[key] = value
        else:
            print(f'Ignoring .env key: {key}')

    for key in default_config:
        config[key] = os.environ.get(key, config[key])

    return config


def main(config):
    """Get latest pipeline-id, builders-job-id and download the artifact"""

    ca_path = config['GLDL_CA_PATH']
    gitlab_api_base_url = config['GLDL_API_BASE_URL']
    gitlab_project_id = config['GLDL_PROJECT_ID']
    gitlab_token = config['GLDL_TOKEN']
    branch = config['GLDL_BRANCH']
    job_name = config['GLDL_JOB_NAME']
    download_path = config['GLDL_DL_PATH']

    if gitlab_token is None or not gitlab_token:
        print('Token is missing. Please set GLDL_TOKEN as env-var!')
        return 1

    api = GitlabApi(
        ca_path=ca_path,
        base_url=gitlab_api_base_url,
        project_id=gitlab_project_id,
        token=gitlab_token,
    )
    api.branch = branch

    try:
        pipeline_id = api.get_pipeline_id()
    except GitlabError as err:
        print(f'Failed to retrieve pipeline-id: {err}')
        return 2

    try:
        job_id = api.get_job_id(pipeline_id, job_name)
    except GitlabError as err:
        print(f'Failed to retrieve job-id: {err}')
        return 3

    try:
        api.ensure_archive_availability(job_id)
    except GitlabError as err:
        print(
            f'Failed to retrieve archive for pipeline {pipeline_id} '
            f'/ job {job_id}: {err}'
        )
        print(
            'Please check if the pipeline of the main branch succeeded lately!'
        )
        return 4

    try:
        api.download_artifact(job_id, download_path)
    except GitlabError as err:
        print(f'Failed to download artifact: {err}')
        return 5

    return 0


if __name__ == '__main__':
    CONFIG = get_config(DEFAULT_CONFIG)

    EXIT_CODE = main(CONFIG)
    sys.exit(EXIT_CODE)

# [EOF]
