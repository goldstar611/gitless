# -*- coding: utf-8 -*-
# Gitless - a version control system built on top of Git
# Licensed under MIT

"""gl resolve - Mark a file with conflicts as resolved."""

from . import file_cmd

parser = file_cmd.parser('mark files with conflicts as resolved', 'resolve', ['rs'])
