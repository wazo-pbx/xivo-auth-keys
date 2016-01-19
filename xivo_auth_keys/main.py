# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import yaml
import xivo_dao

from xivo_dao.helpers.db_utils import session_scope
from xivo_dao.accesswebservice_dao import get_services


def main():
    xivo_dao.init_db_from_config()
    key_updater = _KeyUpdater()

    os.umask(027)
    for service in _get_services():
        key_updater.update(service.login, service.passwd)


def _get_services():
    with session_scope():
        return get_services()


class _KeyUpdater(object):

    filename = '/var/lib/xivo-auth-keys/{service_id}-key.yml'

    def update(self, service_id, service_key):
        filename = self.filename.format(service_id=service_id)
        self._write_config_file(filename, service_id, service_key)

    def _write_config_file(self, filename, service_id, service_key):
        with open(filename, 'w') as fobj:
            yaml.safe_dump({'service_id': service_id,
                            'service_key': service_key}, fobj)
