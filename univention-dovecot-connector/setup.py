# -*- coding: utf-8 -*-

#
# Use only Python 2 and 3 compatible code here!
#

import os
import setuptools

version = os.environ["DOVECOT_PROVISIONING_VERSION"]

setuptools.setup(
    name="univention-dovecot-connector",
    version=version,
    author="Univention GmbH",
    author_email="packages@univention.de",
    description="Cleanup Dovecot Users using Dovecot's doveadm API",
    url="https://www.univention.de/",
    install_requires=['doveadm'],
    packages=["univention.dovecot.connector"],
    license="GNU Affero General Public License v3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
