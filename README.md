# vcsversion

A python library for basing version informatoin for a python project from
the underlying version control system.

vcsversion currently supports git and bzr, but is module so should be able
to support anything. We accept patches.

There are two different contexts from which one might want to call
vcsversion. The first is within setup.py, where you either want to set the
setup version based on VC information or based on a cache file in the
directory. The second is from within your application, where you want to
report the version back.

## Contributing

For information about contributing, visit the project homepage at:

  https://launchpad.net/git-review

For the latest released code, please see PyPI. To get the latest development
source code, please see github at:

  http://github.com/openstack-ci/vcsversion
