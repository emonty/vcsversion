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


def _get_current_tag():
    stat, out = commands.getstatusoutput("bzr tags -r-1")
    if len(out.strip()) == 0:
        return None
    else:
        return out.strip().split()[0]


def _get_bzr_latest_tag():
    tag_info = []
    stat, out = commands.getstatusoutput("bzr tags --sort=time")
    if out.strip() != "":
        return None
    for tag in out.split("\n"):
        tag = tag.strip()
        tag_name, tag_revno = tag.split()
        if tag_revno != "?":
            tag_info.append(tag_name)
    return tag_info[-1]


def _get_bzr_base_version():
    base_version = _get_bzr_latest_tag()
    if base_version is None:
        base_version = "0.0"
    return base_version


def _get_bzr_branch():
    stat, out = commands.getstatusoutput("bzr nick")
    return out.strip()


def _get_bzr_revision_id():
    cmd = "bzr log -r-1 --show-ids"
    stat, out = commands.getstatusoutput(cmd)
    for line in out.split("\n"):
        if line.startswith("revision-id"):
            return line.split()[1]


def _get_bzr_full_revno(before):
    stat, out = commands.getstatusoutput("bzr revno")
    return int(out.strip())


def _get_bzr_revno(before):
    if before:
        # Prefix versioning wants the total number
        return _get_bzr_full_revno()
    else:
        latest_tag = _get_bzr_latest_tag()
        if latest_tag is None:
            return _get_bzr_full_revno()
        else:
            cmd = "bzr log --line -r tag:%s.." % latest_tag
            stat, out = commands.getstatusoutput(cmd)
            if stat != 0:
                # probably a tag in the history on a sub-rev
                return _get_bzr_full_revno()
            log_lines = out.split("\n")
            return len(log_lines) - 1


class bzr(version.version_info):

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
        self.revno = _get_bzr_revno(self.before)
