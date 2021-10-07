#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""Development cycle helper"""

# included batteries
import argparse
import configparser
import os
import sys

# third party
import sh  # pylint: disable=import-error


class ProcessFailed(Exception):
    """Exception for general errors"""


class NetworkUnreachable(Exception):
    """Exception for network errors"""


def section(msg: str):
    """Print a message with a separation line"""

    print(60 * '=')
    print(f'== {msg}')


def update_trigger(sh_out: sh.Command, ucs_host: str):
    """Update the listener_trigger"""

    if ucs_host is None:
        raise ProcessFailed('UCS_HOST not set')

    local_path = 'app/listener_trigger'
    section(f'Finding trigger on "{ucs_host}"')
    if not os.path.exists(local_path):
        raise ProcessFailed(f'file "{local_path}" not found')
    try:
        # pylint: disable=too-many-function-args
        found = sh.ssh(
            ucs_host,
            'find',
            '/var/cache/univention-appcenter',
            '-type f',
            '-mindepth 3',
            '-maxdepth 3',
            '-name dovecot-connector_*.listener_trigger',
        ).split('\n')
    except sh.ErrorReturnCode_255 as err:  # pylint: disable=no-member
        # raised by resolver and network problems
        msg = err.stderr.rstrip().decode('utf-8')
        print(f'Failed to call find via ssh: {msg}')
        raise NetworkUnreachable from err
    except sh.ErrorReturnCode_1 as err:  # pylint: disable=no-member
        # raised if `find` fails
        msg = err.stderr.rstrip().decode('utf-8')
        print(f'Failed to search for the trigger: {msg}')
        raise ProcessFailed from err
    trigger_path = sorted(found)[-1]

    section('Transfering trigger')
    sh_out.scp('-v', local_path, f'{ucs_host}:{trigger_path}')
    return


def build_image(sh_out: sh.Command, image_tag: str, image_path: str):
    """Build the Docker image"""

    section('Building')
    if not os.path.exists('Dockerfile'):
        raise ProcessFailed('file "Dockerfile" not found')
    try:
        sh_out.docker.build(
            f'--build-arg=version={image_tag}', f'--tag={image_path}', '.'
        )
    except sh.ErrorReturnCode_100 as err:  # pylint: disable=no-member
        # build command failed at "apt-get update"
        raise ProcessFailed('docker build failed (100)') from err
    except sh.ErrorReturnCode_125 as err:  # pylint: disable=no-member
        # raised by resolver and network problems
        msg = err.stderr.rstrip().decode('utf-8')
        print(f'Failed to call docker build: {msg}')
        raise ProcessFailed('docker build failed (125)') from err
    except sh.ErrorReturnCode_1 as err:  # pylint: disable=no-member
        raise ProcessFailed('docker build failed (1)') from err
    return


def transfer_image(ussh_out: sh.Command, image_path: str):
    """Transfer image via an ssh-pipe"""

    section('Exporting image to remote host')
    running_command = ussh_out(
        # pylint: disable=no-member
        sh.docker.save(image_path, _piped=True, _err='/dev/stderr'),
        'docker load',
        _iter=True,
    )
    print('Waiting for transfer to finish...')
    try:
        running_command.wait(300)
    except sh.ErrorReturnCode_255 as err:
        # i.e. "No route to host"
        raise ProcessFailed('ssh connection failed') from err
    except sh.TimeoutException as err:
        raise ProcessFailed('image transfer timed out') from err


def reinstall_app(ussh_out: sh.Command):
    """Reinstall the appcenter app"""

    uapp_out = ussh_out.bake('univention-app')
    section('Removing app')
    try:
        uapp_out(
            'remove',
            'dovecot-connector',
            '--do-not-backup',
            '--noninteractive',
        )
    except sh.ErrorReturnCode_255 as err:  # pylint: disable=no-member
        print('App removal failed')
        raise NetworkUnreachable from err
    section('Setting DockerImage')
    uapp_out(
        'dev-set', 'dovecot-connector', 'DockerImage=dovecot-connector:0.0.1'
    )
    section('Installing')
    try:
        uapp_out(
            'install',
            'dovecot-connector',
            '--password=univention',
            '--noninteractive',
            '--do-not-pull-image',
        )
    except sh.ErrorReturnCode_1 as err:
        print('App reinstall failed')
        raise ProcessFailed('uapp install failed') from err


def update_image(
    sh_out: sh.Command, ucs_host: str, image_name: str, image_tag: str
):
    """Call functions for updating the image"""

    if image_name is None:
        raise ProcessFailed('image name not set')
    if image_tag is None:
        raise ProcessFailed('tag not set')
    image_path = f'{image_name}:{image_tag}'
    ussh_out = sh_out.ssh.bake(ucs_host)
    build_image(sh_out, image_tag, image_path)
    transfer_image(ussh_out, image_path)
    reinstall_app(ussh_out)


def update_all(sh_out: sh.Command, **args: dict):
    """Process development steps"""

    update_trigger(sh_out, args['ucs_host'])
    update_image(sh_out, **args)


def not_empty(string):
    """argparse helper to check is string is empty or None"""
    if not string:
        raise argparse.ArgumentTypeError('should not be empty')
    return string


def add_image_arguments(parser, gcfg):
    """Adds argparse arguments for two sub-commands"""

    parser.add_argument(
        '--image',
        dest='image_name',
        default=gcfg.get('image_name'),
        type=not_empty,
        help='image name',
    )
    parser.add_argument(
        '--tag',
        dest='image_tag',
        default=gcfg.get('image_tag'),
        type=not_empty,
        help='tag of the image',
    )


def parse_args(gcfg, args):
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Build and Deploy in a test-environment.'
    )
    subparsers = parser.add_subparsers(dest='sub-command', required=True)

    parser_all = subparsers.add_parser(
        name='all', help='update trigger and image'
    )
    parser_all.set_defaults(func=update_all)
    add_image_arguments(parser_all, gcfg)

    parser_trigger = subparsers.add_parser(
        name='trigger', help='update trigger'
    )
    parser_trigger.set_defaults(func=update_trigger)

    parser_image = subparsers.add_parser(name='image', help='update image')
    parser_image.set_defaults(func=update_image)
    add_image_arguments(parser_image, gcfg)

    parser.add_argument(
        '--host',
        dest='ucs_host',
        default=gcfg.get('ucs_host'),
        type=not_empty,
        help='ucs host',
    )

    args = parser.parse_args(args)
    return vars(args)


def main(base_dir: str, args: list):
    """The main script calls all subfunctions"""

    # pylint: disable=not-callable
    sh_out = sh(_out='/dev/stdout', _err='/dev/stderr', _cwd=base_dir)

    cfg_path = os.path.join(base_dir, 'develop.cfg')
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(cfg_path)

    # need to convert the cfg-object to dict first because otherwise
    # the get-function of configparser tries to call lower on the dict
    gcfg = dict(cfg).get('global', {})

    args = parse_args(gcfg, args)

    # save the func and remove superfluous args
    func = args['func']
    del args['func']
    del args['sub-command']

    try:
        func(sh_out, **args)
    except NetworkUnreachable as err:
        section(f'Processing failed because network is unreachable: {err}')
        return 3
    except ProcessFailed as err:
        section(f'Processing failed: {err}')
        return 2

    section('done')
    return 0


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    try:
        exit_code = main(BASE_DIR, sys.argv[1:])
    except KeyboardInterrupt:
        print('\nStopped by keyboard interrupt')
        exit_code = 1
    sys.exit(exit_code)

# [EOF]
