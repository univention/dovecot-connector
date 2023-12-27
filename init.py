#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

# -*- coding: utf-8 -*-

"""init script for docker"""

from datetime import datetime, timezone
import signal
import sys
import time
import types


def time_stamp():
    """Get an UTC-Timestamp for logs"""
    utc_now = datetime.now(timezone.utc)
    return utc_now.strftime('%Y-%m-%dT%H:%M:%S')


def tprint(message):
    """Print a message with timestamp"""
    print(f'{time_stamp()} init {message}')


def handle_sigterm(signum: int, _: types.FrameType):
    """Handle SIGTERM signal

    Args:
        signum (int): The signals number
        frame (frame): The frame for tracebacks
    """
    signame = signal.Signals(signum).name
    tprint(f'received {signame}')
    sys.exit(100 + signum)


def main():
    """Main function"""
    tprint('start')
    signal.signal(signal.SIGTERM, handle_sigterm)

    while True:
        time.sleep(10)
        tprint('sleeping')

    tprint('end')
    return 0


if __name__ == '__main__':
    try:
        EXIT_CODE = main()
    except KeyboardInterrupt:
        print('init received KeyboardInterrupt')
        EXIT_CODE = 1
    sys.exit(EXIT_CODE)

# [EOF]
