# gym-occupancy
A small scraper to scrape the occupancy of gyms


## Usage

Convert CSV to SQLite using the git history:

```
git-history file occupancy.sqlite occupancy.csv --id gym --csv
```

Conver the SQLite to a pickle file (pkl):

```
python convert_sqlite_to_pkl.py --db occupancy.sqlite --output data.pkl
```