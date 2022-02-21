# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl track - Start tracking changes to files."""

from . import file_cmd

parser = file_cmd.parser('start tracking changes to files', 'track', ['tr'])
