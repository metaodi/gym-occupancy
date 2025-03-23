# -*- coding: utf-8 -*-
"""Hash of a website selector

Usage:
  scrape.py --file <path-to-csv> [--verbose]
  scrape.py (-h | --help)
  scrape.py --version

Options:
  -h, --help                    Show this screen.
  --version                     Show version.
  -f, --file <path-to-csv>    Path to CSV file.
  --verbose                     Option to enable more verbose output.
"""

import logging
import sys
import csv
from bs4 import BeautifulSoup
from docopt import docopt
from lib import download as dl
from datetime import datetime


def get_occupancy(url):
    selector = "[data-visitors]"
    content = dl.download_with_selenium(url, selector)
    soup = BeautifulSoup(content, "html.parser")
    span = soup.select_one(selector)
    if not span:
        log.error(f"Selector {selector} not found in {url}")
        sys.exit(1)
    log.debug(f"span with '{span.text}'")
    try:
        occupancy = int(span.text)
    except ValueError:
        occupancy = None

    return occupancy


def read_from_csv(csv_path):
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def write_to_csv(csv_path, header, rows):
    with open(csv_path, 'w', encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            header,
            delimiter=',',
            quotechar='"',
            lineterminator='\n',
            quoting=csv.QUOTE_NONNUMERIC
        )
        log.info("Start writing CSV")
        writer.writeheader()
        writer.writerows(rows)


log = logging.getLogger(__name__)
arguments = docopt(__doc__, version="Get text from website 1.0")

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.captureWarnings(True)

if arguments["--verbose"]:
    log.setLevel(logging.DEBUG)

file_path = arguments["--file"]
rows = read_from_csv(file_path)
updated_rows = []
for row in rows:
    try:
        row["timestamp_utc"] = datetime.utcnow().isoformat()
        row["occupancy"] = get_occupancy(row["url"])
        row["training_area_m2"] = int(row["training_area_m2"])
    finally:
        updated_rows.append(row)

header = [
    'timestamp_utc',
    'url',
    'training_area_m2',
    'gym',
    'occupancy',
]
write_to_csv(file_path, header, updated_rows)
