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

import vcsversion.build
import optparse


def run():
    base_version = None
    usage = "vcsversion [OPTIONS] ... [BASE_VERSION]"
    parser = optparse.OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) > 0:
        base_version = args[0]
    version_info = vcsversion.build.get_version_info(base_version)
    print version_info.get_branch_nick(), version_info.get_tarball_version()

if __name__ == "__main__":
    run()
