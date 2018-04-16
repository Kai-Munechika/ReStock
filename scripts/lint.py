#!/usr/bin/env python2

# -*- coding: utf-8 -*-
#
# Copyright (C) 2018
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Do *NOT* rename this file to `pylint.py`. Though such is a better name, it
# runs afoul of Python 2 import issues.

import os
from pylint.lint import Run

"""Logic for linting Python files in this application with Pylint."""

def lint():
    """Search for Python source files and lint them with Pylint."""
    # Let's do some prep work before finding files to lint.
    this_dir = os.path.dirname(os.path.realpath(__file__))
    search_paths = (
        this_dir,
        os.path.abspath(os.path.join(this_dir, os.pardir, 'src')),
    )

    # Compile a list of files that need to be linted.
    targets = []
    for search_path in search_paths:
        for root, _, files in os.walk(search_path):
            for file_ in files:
                if file_.endswith('.py'):
                    targets.append(os.path.join(root, file_))

    # All files should be linted at the same time. Doing so allows for summary
    # statistics about all files in this project, and also allows repeated
    # setup/teardown work to be avoided.
    Run(targets)


if __name__ == '__main__':
    lint()
