# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl fetch - A wrapper around git-fetch(1)."""


from ..import core
from . import pprint


def parser(subparsers, _):
    """Adds the fetch parser to the given subparsers object."""
    desc = 'Synchronize branches, tags, references and other meta data from another repository.\n' \
           'For more information on this advanced command refer to the manual page for git-fetch.'
    fetch_parser = subparsers.add_parser(
        'fetch', help=desc, description=desc.capitalize(), aliases=['ft'])
    fetch_parser.set_defaults(func=main)
    fetch_parser.add_argument(
        'fetch_args', nargs="*", help='Additional arguments to pass to `git fetch`')


def main(args, repo):
    p = core.git_wrap('fetch', *args.fetch_args)
    if p.returncode == 0:
        pprint.ok('Fetching from upstream succeeded')
    else:
        pprint.err('Fetching from upstream failed')
    return p.returncode == 0
