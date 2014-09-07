import csv

from models import Trade
from utils import parse_timestamp, parse_date


def load_from_dataset(filename='dataset.csv'):
    """
    Load data from a given CSV file into the NDB Datastore
    """
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next()

        for row in reader:
            date, symbol, timestamp, quote_count, trade_count = row[:5]
            open_px, close_px, high_px, low_px = row[5:]
            timestamp, nanoseconds = parse_timestamp(timestamp)
            kwargs = {
                'date': parse_date(date),
                'symbol': symbol,
                'timestamp': timestamp,
                'timestamp_nanoseconds': int(nanoseconds),
                'quotecount': int(quote_count),
                'tradecount': int(trade_count),
                'openpx': float(open_px),
                'closepx': float(close_px),
                'highpx': float(high_px),
                'lowpx': float(low_px),
            }
            trade = Trade(**kwargs)
            trade.put()


def delete_all():
    """
    Delete all the data from the NDB Datastore
    """
    result = Trade.query()
    for each in result:
        each.key.delete()
