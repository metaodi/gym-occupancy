#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert SQLite db to DataFrame pickle

Usage:
  convert_sqlite_to_pkl.py --db <db-file> --output <pkl-file>
  convert_sqlite_to_pkl.py (-h | --help)
  convert_sqlite_to_pkl.py --version

Options:
  
  -h, --help                   Show this screen.
  --version                    Show version.
  -d, --db <db-file>           Path to the SQLite db file.
  -o, --output <pkl-file>      Path to the output Pickle file.
"""

from docopt import docopt
import sqlite3
import pandas as pd
arguments = docopt(__doc__, version='convert_sqlite_to_pkl.py 1.0')

db = arguments["--db-file"]
pkl = arguments["--pkl-file"]

dat = sqlite3.connect(db)
query = dat.execute("SELECT * From item")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

df.to_pickle(pkl)
