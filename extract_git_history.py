#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract file history from git

Usage:
  extract_git_history.py --file <file-path> --output <output-path>
  extract_git_history.py (-h | --help)
  extract_git_history.py --version

Options:
  
  -h, --help                   Show this screen.
  --version                    Show version.
  -f, --file <file-path>       Path to the git controlled file.
  -o, --output <output-path>   Path to the output file.
"""

from docopt import docopt
import git
import pandas as pd
arguments = docopt(__doc__, version='convert_sqlite_to_pkl.py 1.0')

input_file = arguments["--file"]
output_file = arguments["--output"]
