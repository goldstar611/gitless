# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl patch - A wrapper around git-format-patch(1)."""


from ..import core
from . import pprint

def parser(subparsers, _):
    """Adds the format-patch parser to the given subparsers object."""
    desc = 'Prepare patches for e-mail submission.\n' \
           'For more information on this advanced command refer to the manual page for git-format-patch.'
    patch_parser = subparsers.add_parser(
        'patch', help=desc, description=desc.capitalize(), aliases=['pa'])
    patch_parser.set_defaults(func=main)
    patch_parser.add_argument(
        'patch_args', nargs="*", help='Additional arguments to pass to `git format-patch`')


def main(args, repo):
    p = core.git_wrap('format-patch', *args.patch_args)
    if p.returncode == 0:
        pprint.ok('Creating a patch sucessful')
    else:
        pprint.err('Creating a patch failed')
    return p.returncode == 0
