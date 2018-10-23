# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import os
import pwd
import yaml
import xivo_dao

from xivo_dao.helpers.db_utils import session_scope
from xivo_dao.accesswebservice_dao import get_services

KEYS_PATH = '/var/lib/xivo-auth-keys'
DONT_CHANGE = -1


def main():
    xivo_dao.init_db_from_config()
    key_updater = _KeyUpdater()

    os.umask(027)
    generated_files = []
    for service in _get_services():
        generated_files.append(key_updater.update(service.login, service.passwd))

    _clean_directory(generated_files)


def _get_services():
    with session_scope():
        return get_services()


def _clean_directory(generated_files):
    directory_files = os.listdir(KEYS_PATH)
    for filename in directory_files:
        full_path = os.path.join(KEYS_PATH, filename)
        if full_path not in generated_files:
            os.remove(full_path)


class _KeyUpdater(object):

    filename = os.path.join(KEYS_PATH, '{service_id}-key.yml')

    def __init__(self):
        self._user_map = {pw.pw_name: pw.pw_uid for pw in pwd.getpwall()}

    def update(self, service_id, service_key):
        filename = self.filename.format(service_id=service_id)
        self._write_config_file(filename, service_id, service_key)
        self._change_ownership(filename, service_id)
        return filename

    def _change_ownership(self, filename, service_id):
        uid = self._user_map.get(service_id, DONT_CHANGE)
        os.chown(filename, uid, DONT_CHANGE)

    def _write_config_file(self, filename, service_id, service_key):
        with open(filename, 'w') as fobj:
            yaml.safe_dump({'service_id': service_id,
                            'service_key': service_key}, fobj)
