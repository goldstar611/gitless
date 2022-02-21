# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""Utility library for tests."""

import io
import logging
import os
import re
import shutil
import stat
import sys
import tempfile
import unittest
from locale import getpreferredencoding
from subprocess import run, CalledProcessError

ENCODING = getpreferredencoding() or 'utf-8'


class TestBase(unittest.TestCase):

    def setUp(self, prefix_for_tmp_repo):
        """Creates temporary dir and cds to it."""
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.path = tempfile.mkdtemp(prefix=prefix_for_tmp_repo)
        logging.debug('Created temporary directory {0}'.format(self.path))
        os.chdir(self.path)

    def tearDown(self):
        """Removes the temporary dir."""
        rmtree(self.path)

    def assertRaisesRegexp(self, exc, r, fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
            self.fail('Exception not raised')
        except exc as e:
            msg = e.stderr if isinstance(e, CalledProcessError) else str(e)
            if not re.search(r, msg):
                self.fail('No "{0}" found in "{1}"'.format(r, msg))


def rmtree(path):
    # On Windows, running shutil.rmtree on a folder that contains read-only
    # files throws errors. To workaround this, if removing a path fails, we make
    # the path writable and then try again
    def onerror(func, path, unused_exc_info):  # error handler for rmtree
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            # Swallow errors for now (on Windows there seems to be something weird
            # going on and we can't remove the temp directory even after all files
            # in it have been successfully removed)
            pass

    shutil.rmtree(path, onerror=onerror)
    logging.debug('Removed dir {0}'.format(path))


def symlink(src, dst):
    try:
        os.symlink(src, dst)
    except (AttributeError, NotImplementedError, OSError):
        # Swallow the exceptions, because Windows is very weird about creating
        # symlinks. Python 2 does not have a symlink method on in the os module,
        # AttributeError will handle that. Python 3 does have a symlink method in
        # the os module, however, it has some quirks. NotImplementedError handles
        # the case where the Windows version is prior to Vista. OSError handles the
        # case where python doesn't have permissions to create a symlink on
        # windows. In all cases, it's not necessary to test this, so skip it.
        # See: https://docs.python.org/3.5/library/os.html#os.symlink and
        # https://docs.python.org/2.7/library/os.html#os.symlink for full details.
        pass


def write_file(fp, contents=''):
    _x_file('w', fp, contents=contents)


def append_to_file(fp, contents=''):
    _x_file('a', fp, contents=contents)


def set_test_config():
    git('config', 'user.name', 'test')
    git('config', 'user.email', 'test@test.com')


def read_file(fp):
    with io.open(fp, mode='r', encoding=ENCODING) as f:
        ret = f.read()
    return ret


def git(*args, cwd=None, _in=None):
    p = run(
        ['git', '--no-pager', *args], capture_output=True, check=True, cwd=cwd,
        input=_in, encoding=ENCODING)
    return p.stdout


def gl(*args, cwd=None, _in=None):
    p = run(
        ['gl', *args], capture_output=True, check=True, cwd=cwd,
        input=_in, encoding=ENCODING)
    return p.stdout


# Private functions


def _x_file(x, fp, contents=''):
    if not contents:
        contents = fp
    dirs, _ = os.path.split(fp)
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)
    with io.open(fp, mode=x, encoding=ENCODING) as f:
        f.write(contents)
