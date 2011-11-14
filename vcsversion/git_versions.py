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
    stat, out = commands.getstatusoutput("git tag --contains HEAD")
    if len(out.strip()) == 0:
        return None
    else:
        return out.strip()

def _get_git_base_version():
    tag_info = []
    stat, out = commands.getstatusoutput("git tag")
    if out.strip() != "":
        for tag in out.split("\n"):
            tag = tag.strip()
            cmd = 'git log --format=format:"%%ci %%h %s%%n" -1 %s' % (tag, tag)
            stat, out = commands.getstatusoutput(cmd)
            tag_info.append(out.strip())
        tag_info.sort()
        return tag_info[-1].split()[-1]
    else:
        return "0.0"

def _get_git_branch():
    for branch in commands.getoutput("git branch").split("\n"):
        if branch.startswith('*'):
            return branch.split()[1].strip()
    return "<UNKNOWN>"

def _get_git_revision_id():
    cmd = "git --no-pager log --max-count=1 --pretty=oneline"
    stat, out = commands.getstatusoutput(cmd)
    return out.split()[0]

def _get_git_revno():
    # Expensive. Try not to run this unless we need it
    cmd = "git --no-pager log --oneline"
    stat, out = commands.getstatusoutput(cmd)
    log_lines = out.split("\n")
    return len(log_lines)

class git_versions(versions.versions):

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
                self.base_version = _get_git_base_version()
        else:
            self.before = True
            self.base_version = base_version

        # final gets set if the version we're on is tagged
        self.branch_nick = _get_git_branch()
        self.revision_id = _get_git_revision_id()
        self.revno = None

    def get_revno(self):
        if self.revno is None:
            self.revno = _get_git_revno()
        return self.revno
