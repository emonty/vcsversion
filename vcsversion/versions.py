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

import json
import os

class versions(object):

    def __init__(self, base_version, before=False, final=False,
                 branch_nick=None, revision_id=None, revno=None):
        self.base_version = base
        self.before = before
        # final gets set if the version we're on is tagged
        self.final = final
        self.branch_nick = branch_nick
        self.revno = revno

    def get_base_version(self):
        return self.base_version

    def get_final(self):
        return self.final

    def get_before(self):
        return self.before

    def version_string(self):
        if self.final:
            return self.get_base_version()
        else:
            "%s-dev" % (self.get_base_version(),)

    def get_vcs_version_string(self):
        return '%s:%s' % (self.branch_nick, self.revision_id)

    def version_string_with_vcs(self):
        return '%s-%s' % (self.get_base_version(),
                          self.get_vcs_version_string())

    def get_branch_nick(self):
        return self.branch_nick

    def get_revno(self):
        return self.revno

    def get_revision_id(self):
        return self.revision_id

    def get_tarball_version(self):
        if self.before:
            from datetime import date
            datestamp = date.strftime(date.today(), "%Y%m%d")
            format_str = "%(base_version)s~%(date)s.%(branch_nick)s%(revno)s"
            return format_str % dict(branch_nick=self.get_branch_nick(),
                                     revno=self.get_revno(),
                                     base_version=self.get_base_version(),
                                     date=datestamp)
        else:
            datestamp = None
            return "%s.%s" % (self.get_base_version(),
                              self.get_revno())

    def get_version_dict(self):
        return dict(tarball_version=self.get_tarball_version(),
            revision_id=self.get_revision_id(),
            revno=self.get_revno(),
            branch_nick=self.get_branch_nick(),
            base_version=self.get_base_version(),
            before=self.get_before(),
            final=self.get_final())

    def write_vcsversion(self):
        try:
            with open('.vcsversion','w') as versionfile:
                versionfile.write(json.dumps(self.get_version_dict()))
        except:
            os.remove('.vcsversion')
