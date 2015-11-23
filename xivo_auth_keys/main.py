# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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
import uuid
import yaml


def main():
    key_updater = _KeyUpdater()
    services = ['xivo-agid',
                'xivo-dird-phoned']

    os.umask(027)
    for service in services:
        key_updater.update(service)


class _KeyUpdater(object):

    def __init__(self):
        self.filename = '/var/lib/xivo-auth-keys/{service_id}-key.yml'

    def update(self, service_id):
        filename = self.filename.format(service_id=service_id)
        if not self._is_file_exist(filename):
            service_key = self._generate_key()
            self._write_config_file(filename, service_id, service_key)

    def _generate_key(self):
        return str(uuid.uuid4())

    def _is_file_exist(self, filename):
        return os.path.isfile(filename)

    def _write_config_file(self, filename, service_id, service_key):
        with open(filename, 'w') as fobj:
            yaml.safe_dump({'service_id': service_id,
                            'service_key': service_key}, fobj)
