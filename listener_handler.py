#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Univention Listener Converter
#  Listener integration
#
# Copyright 2021 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.
#

from univention.listener.handler import ListenerModuleHandler
import os
from pathlib import Path
import listener_trigger
import json

DEFAULT_DCC_ADM_HOST = '127.0.0.1'
DEFAULT_DCC_ADM_PORT = 8080
DEFAULT_DCC_ADM_URI = 'http://{DCC_ADM_HOST}:{DCC_ADM_PORT:d}/doveadm/v1'
DEFAULT_DCC_ADM_USERNAME = 'doveadm'
DEFAULT_DCC_ADM_ACCEPTED_EXIT_CODES = '68 75'
DEFAULT_DCC_LOGLEVEL = 'INFO'

# The following settings are this way for compatibility reasons
settings = {
    "dcc_adm_uri": os.environ.get("DCC_ADM_URI", DEFAULT_DCC_ADM_URI),
    "dcc_adm_host": listener_trigger.settings_list(os.environ.get("DCC_ADM_HOST", DEFAULT_DCC_ADM_HOST)),
    "dcc_adm_port": os.environ.get("DCC_ADM_PORT", DEFAULT_DCC_ADM_PORT),
    "dcc_adm_username": os.environ.get("DCC_ADM_USERNAME", DEFAULT_DCC_ADM_USERNAME),
    "dcc_adm_password": os.environ.get("DCC_ADM_PASSWORD", ""),
    "dcc_adm_vmail_template": os.environ.get("DCC_ADM_VMAIL_TEMPLATE", ""),
    "dcc_adm_accepted_exit_codes": set(map(
        int,
        listener_trigger.settings_list(
        os.environ.get(
            "DCC_ADM_ACCEPTED_EXIT_CODES",
            DEFAULT_DCC_ADM_ACCEPTED_EXIT_CODES
            )
        ))),
}

name = 'dovecot-connector'


class DovecotConnectorListenerModule(ListenerModuleHandler):
    def initialize(self):
        self.logger.info('dovecot-connector listener module initialize')

    def create(self, dn, new):
        self.logger.info('[ create ] dn: %r', dn)

    def modify(self, dn, old, new, old_dn):
        self.logger.info('[ modify ] dn: %r', dn)
        if old_dn:
            self.logger.debug('it is (also) a move! old_dn: %r', old_dn)
        self.logger.debug('changed attributes: %r', self.diff(old, new))

    def remove(self, dn, old):
        self.logger.info('[ remove ] dn: %r', dn)
        try:
            listener_trigger.delete_on_all_hosts(
                settings,
                dn,
                old["entryUUID"],
                old
            )
        except Exception as e:
            self.logger.error("Error while deleting mailbox: %s", e)
        

    class Configuration(ListenerModuleHandler.Configuration):
        name = name
        description = 'Handle the removal of mailboxes on LDAP object removal'
        ldap_filter = '(objectClass=person)'
