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
import commands
import setuptools
from setuptools.command.sdist import sdist


def get_version_info(base=None):
    """ factory method which detects and returns the proper driver class """
    if os.path.exists('.git'):
        stat, out = commands.getstatusoutput("git branch")
        if not stat:
            import info.git
            return info.git.git(base)
    if os.path.exists('.bzr'):
        stat, out = commands.getstatusoutput("bzr status")
        if not stat:
            import info.bzr
            return info.bzr.bzr(base)
    if os.path.exists(".vcsversion"):
        import info.cached
        return info.cached.cached(base)


def setup(**kwargs):
    if 'name' in kwargs:
        version_info = get_version_info(kwargs.get('version', None))
    version_info.write_vcsversion()
    kwargs['version'] = version_info.get_tarball_version()
    package_data = kwargs.get("package_data", {})
    empty_package = package_data.get('', [])
    empty_package.append('.vcsversion')
    package_data[''] = empty_package
    kwargs['package_data'] = package_data

    cmdclass_dict = kwargs.get('cmdclass', {})
    sdist_base = cmdclass_dict.get('sdist', sdist)

    class local_sdist(sdist_base):

        def get_file_list(self):
            sdist_base.get_file_list(self)
            self.filelist.append('.vcsversion')
            self.filelist.remove_duplicates()
            self.write_manifest()
    cmdclass_dict['sdist'] = local_sdist
    kwargs['cmdclass'] = cmdclass_dict
    return setuptools.setup(
        include_package_data=True,
        **kwargs)
