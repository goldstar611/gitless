# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl ignore - Appends a pattern to the .gitignore file in current working directory (default) or repo root (global)."""

import os
import pathlib


def parser(subparsers, _):
    """Adds the ignore parser to the given subparsers object."""
    desc = 'Appends a pattern to the .gitignore file in current working directory (default) or repo root (global)'
    ignore_parser = subparsers.add_parser(
        'ignore', help=desc, description=desc.capitalize(), aliases=['ig'])
    ignore_parser.add_argument(
        'ignored_list', nargs='*', help='ignored file pattern', metavar='file_pattern')
    ignore_parser.add_argument(
        '-g', '--global', dest='ignore_global',
        help='add the file patterns to the .gitignore file at the repo root, not current working directory',
        action='store_true')
    ignore_parser.set_defaults(func=main)


def main(args, repo):
    ret = True
    if args.ignored_list:
        if args.ignore_global:
            git_ignore_file = pathlib.Path(repo.git_repo.workdir) / ".gitignore"
        else:
            git_ignore_file = ".gitignore"

        with open(git_ignore_file, "at") as f:
            f.write("{0}# Ignored by gitless cli{0}".format(os.linesep))
            for pattern in args.ignored_list:
                f.write("{0}{1}".format(pattern, os.linesep))

    return ret
