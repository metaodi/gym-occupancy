import csv
from io import StringIO
import logging
log = logging.getLogger(__name__)


def read_from_csv(csv_path):
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def read_from_csv_string(content):
    rows = []
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))
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
