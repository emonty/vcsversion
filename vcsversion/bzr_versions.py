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

import versions
import commands

def _get_current_tag():
    stat, out = commands.getstatusoutput("bzr tags -r-1")
    if len(out.strip()) == 0:
        return None
    else:
        return out.strip().split()[0]

def _get_bzr_base_version():
    tag_info = []
    stat, out = commands.getstatusoutput("bzr tags --sort=time")
    for tag in out.split("\n"):
        tag = tag.strip()
        tag_name, tag_revno = tag.split()
        if tag_revno != "?":
            tag_info.append(tag_name)
    return tag_info[-1]

def _get_bzr_branch():
    stat, out = commands.getstatusoutput("bzr nick")
    return out.strip()

def _get_bzr_revision_id():
    cmd = "bzr log -r-1 --show-ids"
    stat, out = commands.getstatusoutput(cmd)
    for line in out.split("\n"):
        if line.startswith("revision-id"):
            return line.split()[1]

def _get_bzr_revno():
    stat, out = commands.getstatusoutput("bzr revno")
    return out.strip()

class bzr_versions(versions.versions):

    def __init__(self, base_version=None):
        self.current_tag = _get_current_tag()
        if self.current_tag is None:
            self.final = False
        else:
            self.final = True

        if base_version is None:
            self.before = False
            if self.final:
                self.base_version = self.current_tag
            else:
                self.base_version = _get_bzr_base_version()
        else:
            self.before = True
            self.base_version = base_version

        # final gets set if the version we're on is tagged
        self.branch_nick = _get_bzr_branch()
        self.revision_id = _get_bzr_revision_id()
        self.revno = _get_bzr_revno()

