# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""Module for pretty printing Gitless output."""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from datetime import datetime, tzinfo, timedelta
from locale import getpreferredencoding
import re
import sys

DISABLE_COLOR = False

from gitless import core

SEP = (
    '##########################################################################'
    '######')

ENCODING = getpreferredencoding() or 'utf-8'


def puts(s='', newline=True, stream=sys.stdout.write):
    if newline:
        s = s + '\n'
    stream(s)


# Colored strings
RED = '\033[91m'
RED_BOLD = '\033[1;91m'
GREEN = '\033[32m'
GREEN_BOLD = '\033[1;32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
CLEAR = '\033[0m'


def _color(color_code, text):
    return '{0}{1}{2}'.format(color_code, text, CLEAR) if should_color() else text


def should_color():
    # We only output colored lines if the coloring is enabled and we are not being
    # piped or redirected
    return not DISABLE_COLOR and sys.stdout.isatty()


def red(text):
    return _color(RED, text)


def green(text):
    return _color(GREEN, text)


def yellow(text):
    return _color(YELLOW, text)


def blue(text):
    return _color(BLUE, text)


def magenta(text):
    return _color(MAGENTA, text)


def cyan(text):
    return _color(CYAN, text)


# Stdout


def ok(text):
    puts(green('✔ {0}'.format(text)))


def warn(text):
    puts(yellow('! {0}'.format(text)))


def msg(text, stream=sys.stdout.write):
    puts(text, stream=stream)


def exp(text, stream=sys.stdout.write):
    puts('  ➜ {0}'.format(text), stream=stream)


def item(i, opt_text='', stream=sys.stdout.write):
    puts('    {0}{1}'.format(i, opt_text), stream=stream)


def blank(stream=sys.stdout.write):
    puts('', stream=stream)


def sep(stream=sys.stdout.write):
    puts(SEP, stream=stream)


# Err

def err(text):
    puts(red('✘ {0}'.format(text)), stream=sys.stderr.write)


def err_msg(text):
    msg(text, stream=sys.stderr.write)


def err_exp(text):
    exp(text, stream=sys.stderr.write)


def err_blank():
    blank(stream=sys.stderr.write)


def err_item(i, opt_text=''):
    item(i, opt_text, stream=sys.stderr.write)


# Misc

def conf_dialog(text):
    """Gets confirmation from the user.

    Prints a confirmation message to stdout with the given text and waits for
    user confirmation.

    Args:
      text: the text to include in the confirmation.

    Returns:
      True if the user confirmed she wanted to continue or False if otherwise.
    """
    msg('{0}. Do you wish to continue? (y/N)'.format(text))
    user_input = get_user_input()
    return user_input and user_input[0].lower() == 'y'


def get_user_input(text='> '):
    """Python 2/3 compatible way of getting user input."""
    global input
    try:
        # Disable pylint's redefined-builtin warning and undefined-variable
        # (raw_input is undefined in python 3) error.
        # pylint: disable=W0622
        # pylint: disable=E0602
        input = raw_input
    except NameError:
        pass
    return input(text)


def commit_str(ci):
    ci_str = StringIO()
    commit(ci, compact=True, stream=ci_str.write)
    return ci_str.getvalue().strip()


def commit(ci, compact=False, stream=sys.stdout.write, line_additions=0, line_deletions=0):
    merge_commit = len(ci.parent_ids) > 1
    color = magenta if merge_commit else yellow
    if compact:
        title = ci.message.splitlines()[0]
        puts('{0} {1}'.format(color(str(ci.id)[:7]), title), stream=stream)
        return
    puts(color('Commit Id: {0}'.format(ci.id)), stream=stream)
    if merge_commit:
        merges_str = ' '.join(str(oid)[:7] for oid in ci.parent_ids)
        puts(color('Merges:    {0}'.format(merges_str)), stream=stream)
    puts(
        color('Author:    {0} <{1}>'.format(ci.author.name, ci.author.email)),
        stream=stream)
    ci_author_dt = datetime.fromtimestamp(
        ci.author.time, FixedOffset(ci.author.offset))
    puts(color('Date:      {0:%c %z}'.format(ci_author_dt)), stream=stream)
    put_s = lambda num: '' if num == 1 else 's'
    puts(color('Stats:     {0} line{1} added, {2} line{3} removed'
               .format(line_additions, put_s(line_additions),
                       line_deletions, put_s(line_deletions))), stream=stream)
    puts(stream=stream)
    puts('    {0}'.format(ci.message), stream=stream)


# Op Callbacks

def apply_ok(ci):
    ok('Insertion of {0} succeeded'.format(ci.id))
    blank()
    commit(ci)
    blank()


def apply_err(ci):
    err('Insertion of {0} failed'.format(ci.id))
    blank()
    commit(ci)
    blank()


def save():
    warn('Temporarily saving uncommitted changes')


def restore_ok():
    ok('Uncommitted changes applied successfully to the new head of the branch')


OP_CB = core.OpCb(apply_ok, apply_err, save, restore_ok)


class FixedOffset(tzinfo):

    def __init__(self, offset):
        super(FixedOffset, self).__init__()
        self.__offset = timedelta(minutes=offset)

    def utcoffset(self, _):
        return self.__offset

    def dst(self, _):
        return timedelta(0)


def diff(patch, stream=sys.stdout.write):
    # Diff header

    old_fp = patch.delta.old_file.path
    new_fp = patch.delta.new_file.path
    puts('Diff of file "{0}"'.format(old_fp), stream=stream)
    if old_fp != new_fp:
        puts(cyan(' (renamed to {0})'.format(new_fp)), stream=stream)
        puts(stream=stream)

    if patch.delta.is_binary:
        puts('Not showing diffs for binary file', stream=stream)
        return

    additions = patch.line_stats[1]
    deletions = patch.line_stats[2]
    if (not additions) and (not deletions):
        puts('No diffs to output for file', stream=stream)
        return

    put_s = lambda num: '' if num == 1 else 's'
    puts('{0} line{1} added'.format(additions, put_s(additions)), stream=stream)
    puts('{0} line{1} removed'.format(deletions, put_s(deletions)), stream=stream)
    puts(stream=stream)

    # Diff body

    for hunk in patch.hunks:
        puts(stream=stream)
        _hunk(hunk, stream=stream)

    puts(stream=stream)
    puts(stream=stream)


def diff_totals(total_additions, total_deletions, stream=sys.stdout.write):
    put_s = lambda num: '' if num == 1 else 's'
    puts('Diff summary', stream=stream)
    puts('Total of {0} line{1} added'
         .format(total_additions, put_s(total_additions)), stream=stream)
    puts('Total of {0} line{1} removed'
         .format(total_deletions, put_s(total_deletions)), stream=stream)
    puts(stream=stream)


def _hunk(hunk, stream=sys.stdout.write):
    puts(cyan('@@ -{0},{1} +{2},{3} @@'.format(
        hunk.old_start, hunk.old_lines, hunk.new_start, hunk.new_lines)),
        stream=stream)
    padding = _padding(hunk)

    del_line, add_line, maybe_bold, saw_add = None, None, False, False
    for diff_line in hunk.lines:
        st = diff_line.origin

        if st == '-' and not maybe_bold:
            maybe_bold = True
            del_line = diff_line
        elif st == '+' and maybe_bold and not saw_add:
            saw_add = True
            add_line = diff_line
        elif st == ' ' and maybe_bold and saw_add:
            bold1, bold2 = _highlight(del_line.content, add_line.content)

            puts(_format_line(del_line, padding, bold_delim=bold1), stream=stream)
            puts(_format_line(add_line, padding, bold_delim=bold2), stream=stream)

            del_line, add_line, maybe_bold, saw_add = None, None, False, False

            puts(_format_line(diff_line, padding), stream=stream)
        else:
            if del_line:
                puts(_format_line(del_line, padding), stream=stream)
            if add_line:
                puts(_format_line(add_line, padding), stream=stream)

            del_line, add_line, maybe_bold, saw_add = None, None, False, False

            puts(_format_line(diff_line, padding), stream=stream)

    if maybe_bold and saw_add:
        bold1, bold2 = _highlight(del_line.content, add_line.content)

        puts(_format_line(del_line, padding, bold_delim=bold1), stream=stream)
        puts(_format_line(add_line, padding, bold_delim=bold2), stream=stream)
    else:
        if del_line:
            puts(_format_line(del_line, padding), stream=stream)
        if add_line:
            puts(_format_line(add_line, padding), stream=stream)


def _padding(hunk):
    MIN_LINE_PADDING = 8

    max_line_number = max([
        hunk.old_start + hunk.old_lines, hunk.new_start + hunk.new_lines])
    max_line_digits = len(str(max_line_number))
    return max(MIN_LINE_PADDING, max_line_digits + 1)


def _format_line(diff_line, padding, bold_delim=None):
    """Format a standard diff line.

    Returns:
      a padded and colored version of the diff line with line numbers
    """
    if should_color():
        green = GREEN
        green_bold = GREEN_BOLD
        red = RED
        red_bold = RED_BOLD
        clear = CLEAR
    else:
        green = ''
        green_bold = ''
        red = ''
        red_bold = ''
        clear = ''

    formatted = ''
    st = diff_line.origin
    line = st + diff_line.content.rstrip('\n')
    old_lineno = diff_line.old_lineno
    new_lineno = diff_line.new_lineno

    if st == ' ':
        formatted = (
                str(old_lineno).ljust(padding) + str(new_lineno).ljust(padding) + line)
    elif st == '+':
        formatted = ' ' * padding + green + str(new_lineno).ljust(padding)
        if not bold_delim:
            formatted += line
        else:
            bold_start, bold_end = bold_delim
            formatted += (
                    line[:bold_start] + green_bold + line[bold_start:bold_end] + clear +
                    green + line[bold_end:])
    elif st == '-':
        formatted = red + str(old_lineno).ljust(padding) + ' ' * padding
        if not bold_delim:
            formatted += line
        else:
            bold_start, bold_end = bold_delim
            formatted += (
                    line[:bold_start] + red_bold + line[bold_start:bold_end] + clear +
                    red + line[bold_end:])

    return formatted + clear


def _highlight(line1, line2):
    """Returns the sections that should be bolded in the given lines.

    Returns:
      two tuples. Each tuple indicates the start and end of the section
      of the line that should be bolded for line1 and line2 respectively.
     """
    start1 = start2 = 0
    match = re.search(r'\S', line1)  # ignore leading whitespace
    if match:
        start1 = match.start()
    match = re.search(r'\S', line2)
    if match:
        start2 = match.start()
    length = min(len(line1), len(line2)) - 1
    bold_start1 = start1
    bold_start2 = start2
    while (bold_start1 <= length and bold_start2 <= length and
           line1[bold_start1] == line2[bold_start2]):
        bold_start1 += 1
        bold_start2 += 1
    match = re.search(r'\s*$', line1)  # ignore trailing whitespace
    bold_end1 = match.start() - 1
    match = re.search(r'\s*$', line2)
    bold_end2 = match.start() - 1
    while (bold_end1 >= bold_start1 and bold_end2 >= bold_start2 and
           line1[bold_end1] == line2[bold_end2]):
        bold_end1 -= 1
        bold_end2 -= 1
    if bold_start1 - start1 > 0 or len(line1) - 1 - bold_end1 > 0:
        return (bold_start1 + 1, bold_end1 + 2), (bold_start2 + 1, bold_end2 + 2)
    return None, None
