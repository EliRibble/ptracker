#!/usr/bin/env python
try:
    from setuptools import setup
    extra = dict(include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

import os
import sys
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
import ptracker
assert os.path.abspath(os.path.join(ROOT_DIR, 'ptracker', '__init__.py')) in ptracker.__file__

def do_setup(current_version):
    files = ['ptracker/*']

    setup(  name                = 'ptracker',
            version             = current_version,
            description         = "A system for communicating with PivotalTracker",
            long_description    = open("README.rst").read(),
            author              = "HireVue, Inc.",
            author_email        = 'eribble@hirevue.com',
            install_requires    = ['argparse>=1.2.1'],
            packages            = ['ptracker'],
            package_data        = {'ptracker': files},
            scripts             = ['bin/ptracker'],
            **extra
    )

def get_current_version(release):
    try:
        import version
        current_version = version.get_git_version(release=release)
        with open('ptracker/__init__.py', 'w') as init:
            init.write("VERSION = '{0}'\n".format(current_version))
        print("Wrote ptracker/__init__.py with version {0}".format(current_version))
        return current_version
    except ImportError:
        return ptracker.VERSION

def main():
    release = os.environ.get('RELEASE', False)
    try:
        release = int(release) != 0
    except ValueError:
        print("Ignoring release value of '{0}'. It should be a nonzero integer to specify a release build".format(release))
        release = False

    current_version = get_current_version(release)
    do_setup(current_version)
        
if __name__ == '__main__':
    main()
