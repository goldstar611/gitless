# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl remote - List, create, edit or delete remotes."""

from . import pprint


def parser(subparsers, _):
    """Adds the remote parser to the given subparsers object."""
    desc = 'list, create, edit or delete remotes'
    remote_parser = subparsers.add_parser(
        'remote', help=desc, description=desc.capitalize(), aliases=['rt'])
    remote_parser.add_argument(
        '-c', '--create', nargs='?', help='create remote', dest='remote_name',
        metavar='remote')
    remote_parser.add_argument(
        'remote_url', nargs='?',
        help='the url of the remote (only relevant if a new remote is created)')
    remote_parser.add_argument(
        '-d', '--delete', nargs='+', help='delete remote(es)', dest='delete_r',
        metavar='remote')
    remote_parser.add_argument(
        '-u', '--update', nargs='+', help='update remote URL', dest='update_r',
        metavar='remote')
    remote_parser.add_argument(
        '-rn', '--rename', nargs='+',
        help='renames the specified remote: accepts two arguments '
             '(current remote name and new remote name)',
        dest='rename_r')
    remote_parser.set_defaults(func=main)


def main(args, repo):
    ret = True
    remotes = repo.remotes
    if args.remote_name:
        if not args.remote_url:
            raise ValueError('Missing url')
        ret = _do_create(args.remote_name, args.remote_url, remotes)
    elif args.delete_r:
        ret = _do_delete(args.delete_r, remotes)
    elif args.update_r:
        ret = _do_update(args.update_r, remotes)
    elif args.rename_r:
        ret = _do_rename(args.rename_r, remotes)
    else:
        ret = _do_list(remotes)

    return ret


def _do_list(remotes):
    pprint.msg('List of remotes:')
    pprint.exp('do gl remote -c r r_url to add a new remote r mapping to r_url')
    pprint.exp('do gl remote -u r r_url to update an existing remote to r_url')
    pprint.exp('do gl remote -d r to delete remote r')
    pprint.blank()

    if not len(remotes):
        pprint.item('There are no remotes to list')
    else:
        for r in remotes:
            pprint.item(r.name, opt_text=' (maps to {0})'.format(r.url))
    return True


def _do_create(rn, ru, remotes):
    remotes.create(rn, ru)
    pprint.ok('Remote {0} mapping to {1} created successfully'.format(rn, ru))
    pprint.exp('to list existing remotes do gl remote')
    pprint.exp('to remove {0} do gl remote -d {1}'.format(rn, rn))
    return True


def _do_delete(delete_r, remotes):
    errors_found = False

    for r in delete_r:
        try:
            remotes.delete(r)
            pprint.ok('Remote {0} removed successfully'.format(r))
        except KeyError:
            pprint.err('Remote \'{0}\' doesn\'t exist'.format(r))
            errors_found = True
    return not errors_found


def _do_rename(rename_r, remotes):
    errors_found = False
    if len(rename_r) != 2:
        pprint.err(
            'Expected 2 arguments in the following format: '
            'gl remote -rn current_remote_name new_remote_name')
        errors_found = True
    else:
        try:
            remotes.rename(rename_r[0], rename_r[1])
            pprint.ok('Renamed remote {0} to {1}'.format(rename_r[0], rename_r[1]))
        except KeyError:
            pprint.err('Remote \'{0}\' doesn\'t exist'.format(rename_r[0]))
            errors_found = True
    return not errors_found


def _do_update(update_r, remotes):
    errors_found = False
    if len(update_r) != 2:
        pprint.err(
            'Expected 2 arguments in the following format: '
            'gl remote -u remote_name https://new_remote_url')
        errors_found = True
    else:
        try:
            remotes.set_url(update_r[0], update_r[1])
            pprint.ok('Updated remote {0} URL to {1}'.format(update_r[0], update_r[1]))
        except KeyError:
            pprint.err('Remote \'{0}\' doesn\'t exist'.format(update_r[0]))
            errors_found = True
    return not errors_found
