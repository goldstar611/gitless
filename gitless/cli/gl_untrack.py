# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl untrack - Stop tracking changes to files."""

from . import file_cmd

parser = file_cmd.parser('stop tracking changes to files', 'untrack', ['un'])
