# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl revert - A wrapper around git-revert1)."""


from ..import core
from . import pprint

def parser(subparsers, _):
    """Adds the revert parser to the given subparsers object."""
    desc = 'Revert some existing commits.\n' \
           'For more information on this advanced command refer to the manual page for git-revert.'
    revert_parser = subparsers.add_parser(
        'revert', help=desc, description=desc.capitalize(), aliases=['re'])
    revert_parser.set_defaults(func=main)
    revert_parser.add_argument(
        'revert_args', nargs="*", help='Additional arguments to pass to `git revert`')


def main(args, repo):
    p = core.git_wrap('revert', *args.revert_args)
    if p.returncode == 0:
        pprint.ok('Reverting commit sucessful')
    else:
        pprint.err('Reverting commit failed')
    return p.returncode == 0
