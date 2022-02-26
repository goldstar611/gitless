# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl pull - A wrapper around git-pull(1)."""


from ..import core
from . import pprint


def parser(subparsers, _):
    """Adds the pull parser to the given subparsers object."""
    desc = 'Synchronize and merges branches, tags, references and other meta data from mirror repository.\n' \
           'For more information on this advanced command refer to the manual page for git-pull.'
    pull_parser = subparsers.add_parser(
        'pull', help=desc, description=desc.capitalize(), aliases=['pl'])
    pull_parser.set_defaults(func=main)
    pull_parser.add_argument(
        'pull_args', nargs="*", help='Additional arguments to pass to `git pull`')


def main(args, repo):
    p = core.git_wrap('pull', *args.pull_args)
    if p.returncode == 0:
        pprint.ok('Pulling from your mirror succeeded')
    else:
        pprint.err('Pulling from your mirror failed')
