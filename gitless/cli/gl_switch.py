# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl switch - Switch branches."""

from . import pprint


def parser(subparsers, _):
    """Adds the switch parser to the given subparsers object."""
    desc = 'switch branches'
    switch_parser = subparsers.add_parser(
        'switch', help=desc, description=desc.capitalize(), aliases=['sw'])
    switch_parser.add_argument('branch', help='switch to branch')
    switch_parser.add_argument(
        '-mo', '--move-over',
        help='move uncomitted changes made in the current branch to the '
             'destination branch',
        action='store_true')
    switch_parser.add_argument('-mi', '--move-ignored',
                               help='move ignored files to the destination branch, '
                                    'has no effect if --move-over is also set',
                               action='store_true')
    switch_parser.set_defaults(func=main)


def main(args, repo):
    b = repo.lookup_branch(args.branch)

    if not b:
        pprint.err('Branch {0} doesn\'t exist'.format(args.branch))
        pprint.err_exp('to list existing branches do gl branch')
        pprint.err_exp('to create a new branch do gl branch -c {0}'.format(args.branch))
        return False

    repo.switch_current_branch(b, move_over=args.move_over, move_ignored=args.move_ignored)
    pprint.ok('Switched to branch {0}'.format(args.branch))
    return True
