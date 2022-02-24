#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
import re
import sys

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('gitless/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# Build helper
if sys.argv[-1] == 'gl-build':
    from subprocess import run
    import shutil
    import tarfile
    import platform

    rel = 'gl-v{0}-{1}-{2}'.format(
        version, platform.system().lower(), platform.machine())

    print('running pyinstaller...')
    run(
        ['pyinstaller', 'gl.spec', '--clean', '--distpath', rel],
        stdout=sys.stdout, stderr=sys.stderr)
    print('success!! gl binary should be at {0}/gl'.format(rel))

    print('creating tar.gz file')
    shutil.copy('README.md', rel)
    shutil.copy('LICENSE.md', rel)

    with tarfile.open(rel + '.tar.gz', 'w:gz') as tar:
        tar.add(rel)
    print('success!! binary release at {0}'.format(rel + '.tar.gz'))

    sys.exit()

ld = """
Installing Gitless won't interfere with your Git installation in any
way. You can keep using Git and switch between Git and Gitless seamlessly.
It features a simple commit workflow, independent branches, and
a friendly command-line interface. Because Gitless is implemented on top of
Git, you can always fall back to the Git command line interface.

More info, downloads and documentation @ The `Gitless
website <http://gitless.com>`__.
"""

setup(
    name='gitless',
    version=version,
    description='A maintained simple interface to git operations',
    long_description=ld,
    author='Santiago Perez De Rosso',
    author_email='sperezde@csail.mit.edu',
    maintainer='@goldstar611',
    url='https://github.com/goldstar611/gitless',
    packages=['gitless', 'gitless.cli'],
    install_requires=[
        # make sure install_requires is consistent with requirements.txt
        'pygit2>=1.4.0',  # requires libgit2 1.1.x
        'argcomplete>=1.11.1'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control'],
    entry_points={
        'console_scripts': [
            'gl = gitless.cli.gl:main'
        ]},
    test_suite='gitless.tests')
