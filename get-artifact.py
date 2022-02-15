#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Download an artifact from a different Gitlab project
"""

# included batteries
from datetime import datetime, timezone
import os
import sys

# 3rd-pary
import requests

DEFAULT_API_BASE_URL = 'https://git.knut.univention.de/api/v4'
DEFAULT_CA_PATH = '/etc/ssl/certs/ca-certificates.crt'
DEFAULT_DL_PATH = 'artifact.zip'


class GitlabError(Exception):
    """Gitlab REST error"""


class GitlabApi:
    """Handle REST calls to the Gitlab API"""
    def __init__(self, ca_path, base_url, project_id, token):
        self.base_url = base_url
        self.project_id = project_id
        self.session = requests.session()
        self.session.headers.update({'PRIVATE-TOKEN': token})
        self.session.verify = ca_path

    def get_pipeline_id(self, branch='main'):
        """Get the latest pipeline-id of a given branch"""
        pipelines_url = f'{self.base_url}/projects/{self.project_id}/pipelines'
        params = {'ref': branch, 'per_page': 1}
        response = self.session.get(pipelines_url, params=params)
        content = response.json()
        if response.status_code == 401:
            print(f"Message: {content['message']}")
            raise GitlabError('Bad authorization. Check token!')
        if response.status_code == 404:
            print(f"Message: {content['message']}")
            raise GitlabError('Project not found')
        if response.status_code != 200:
            print(f"Message: {content['message']}")
            raise GitlabError(f'Request failed with {response.status_code}')
        pipeline_id = response.json()[0]['id']
        return pipeline_id

    def get_job_id(self, pipeline_id, job_name='build-job'):
        """Get a job-id by job-name of a given pipeline-id"""
        jobs_url = (
            f'{self.base_url}/projects/{self.project_id}'
            f'/pipelines/{pipeline_id}/jobs'
        )
        response = self.session.get(jobs_url)
        if response.status_code != 200:
            raise GitlabError(f'Request failed with {response.status_code}')
        jobs = response.json()
        for job in jobs:
            if job['name'] == job_name:
                job_id = job['id']
        return job_id

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
            time_left = artifacts_expire_at - datetime.utcnow().replace(tzinfo=timezone.utc)
            seconds_left = time_left.total_seconds()
            if seconds_left < 0:
                raise GitlabError('artifacts expired')
        return

    def download_artifact(self, job_id, download_path=DEFAULT_DL_PATH):
        """Download the artifact zip-file of a given job"""
        artifacts_url = (
            f'{self.base_url}/projects/{self.project_id}'
            f'/jobs/{job_id}/artifacts'
        )
        with self.session.get(artifacts_url, stream=True) as response:
            if response.status_code != 200:
                raise GitlabError(
                    f'Request failed with {response.status_code}'
                )
            with open(download_path, 'wb') as buffered_writer:
                for chunk in response.iter_content(chunk_size=8192):
                    buffered_writer.write(chunk)
        return


def main(
    ca_path,
    gitlab_api_base_url,
    gitlab_project_id,
    gitlab_token,
    download_path,
):
    """Get latest pipeline-id, builders-job-id and download the artifact"""
    if gitlab_token is None or not gitlab_token:
        print('Token is missing. Please set GLDL_TOKEN as env-var!')
        return 1

    api = GitlabApi(
        ca_path, gitlab_api_base_url, gitlab_project_id, gitlab_token
    )

    try:
        pipeline_id = api.get_pipeline_id()
    except GitlabError as err:
        print(f'Failed to retrieve pipeline-id: {err}')
        return 2

    try:
        job_id = api.get_job_id(pipeline_id)
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
    GLDL_CA_PATH = os.environ.get('GLDL_CA_PATH', DEFAULT_CA_PATH)
    GLDL_API_BASE_URL = os.environ.get(
        'GLDL_API_BASE_URL', DEFAULT_API_BASE_URL
    )
    GLDL_PROJECT_ID = os.environ.get('GLDL_PROJECT_ID', 1)
    GLDL_TOKEN = os.environ.get('GLDL_TOKEN')
    GLDL_DL_PATH = os.environ.get('GLDL_DL_PATH', DEFAULT_DL_PATH)
    EXIT_CODE = main(
        GLDL_CA_PATH,
        GLDL_API_BASE_URL,
        GLDL_PROJECT_ID,
        GLDL_TOKEN,
        GLDL_DL_PATH,
    )
    sys.exit(EXIT_CODE)

# [EOF]
