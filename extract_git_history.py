#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract file history from git

Usage:
  extract_git_history.py --input <file-path> --output <output-path> [--start-at <commit>]
  extract_git_history.py (-h | --help)
  extract_git_history.py --version

Options:
  -h, --help                    Show this screen.
  --version                     Show version.
  -i, --input <file-path>       Path to the git controlled file.
  -o, --output <output-path>    Path to the output file.
  -s, --start-at <commit>       SHA of the start commit.

"""

import os
from docopt import docopt
import git
import pandas as pd
from pathlib import Path
import csv
from lib import utils


arguments = docopt(__doc__, version='extract_git_history.py 1.0')


def iterate_file_versions(filepath, start_commit=None):
    ref = "main"
    relative_path = str(Path(filepath).relative_to('.'))
    repo = git.Repo('.', odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref, paths=[relative_path])))
    for commit in commits:
        try:
            content = commit.tree[relative_path].data_stream.read()
            yield commit.committed_datetime, commit.hexsha, content
        except KeyError:
            # This commit doesn't have a copy of the requested file
            pass

input_file = arguments["--input"]
output_file = arguments["--output"]
start_at = arguments["--start-at"]

all_rows = []

if start_at:
   start = False
else:
    start = True

for git_commit_at, git_hash, content in iterate_file_versions(input_file):
    if git_hash == start_at:
        start = True
    if start:
        version_rows = utils.read_from_csv_string(content)
        all_rows.extend(version_rows)

header = [
    'timestamp_utc',
    'url',
    'training_area_m2',
    'gym',
    'occupancy',
]
utils.write_to_csv(output_file, header, all_rows)
