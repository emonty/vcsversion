# vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright 2011 OpenStack LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import version
import commands
import json


class cached(version.version_info):

    def __init__(self, base):
        with open(".vcsversion", "r") as versioninfo:
            _versions = json.load(versioninfo)

        self.revno = _versions['revno']
        self.revision_id = _versions['revision_id']
        self.revindex = _versions['revindex']
        self.branch_nick = _versions['branch_nick']
        self.base_version = _versions['base_version']
        self.final = _versions['final']
        self.before = _versions['before']

    @staticmethod
    def write_vcsversion():
        pass
