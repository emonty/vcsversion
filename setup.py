#!/usr/bin/python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright (c) 2010-2011 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from setuptools import find_packages

from vcsversion import build

build.setup(
    name='vcsversion',
    description="Library for managing version information from VCS",
    license='Apache License (2.0)',
    classifiers=["Programming Language :: Python"],
    keywords='git bzr version',
    author='OpenStack, LLC.',
    author_email='openstack@lists.launchpad.net',
    url='https://launchpad.net/vcsversion',
    install_requires=['distribute'],
    packages=find_packages(exclude=['test', 'bin']),
    entry_points={
        'console_scripts': [
            'vcsversion = vcsversion.cmd:run',
        ],
    }
)
