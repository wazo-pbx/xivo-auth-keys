#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import setup, find_packages


setup(
    name='xivo_auth_keys',
    version='0.1',

    description='XiVO auth keys',

    author='Wazo Authors',
    author_email='dev@wazo.community',

    url='http://wazo.community',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'xivo-update-keys = xivo_auth_keys.main:main',
        ],
    }
)
