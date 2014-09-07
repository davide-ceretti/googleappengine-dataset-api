import datetime

from models import Trade
from scripts import load_from_dataset, delete_all
from tests.utils import NDBTestCase


class TestLoadFromDatabase(NDBTestCase):
    def test_default_dataset_can_be_loaded(self):
        load_from_dataset()
        self.assertEqual(Trade.query().count(), 512)

    def test_example_csv(self):
        """
        Date,Symbol,TimeStamp,QuoteCount,TradeCount,OpenPx,ClosePx,HighPx,LowPx
        20130719,LFZ,2013-07-19 08:47:00.000457891,304,24,6387.0000000,
        6386.5000000,6387.0000000,6386.0000000
        """
        load_from_dataset('tests/example.csv')

        trade = Trade.query().get()

        self.assertEqual(trade.date, datetime.date(2013, 7, 19))
        self.assertEqual(trade.symbol, 'LFZ')
        self.assertEqual(
            trade.timestamp, datetime.datetime(2013, 7, 19, 8, 47, 0)
        )
        self.assertEqual(trade.timestamp_nanoseconds, 457891)
        self.assertEqual(trade.quotecount, 304)
        self.assertEqual(trade.tradecount, 24)
        self.assertEqual(trade.openpx, 6387.0000000)
        self.assertEqual(trade.closepx, 6386.5000000)
        self.assertEqual(trade.highpx, 6387.0000000)
        self.assertEqual(trade.lowpx, 6386.0000000)


class TestDeleteAll():
    def test_trades_are_deleted(self):
        load_from_dataset('tests/example.csv')
        self.assertEqual(Trade.query().count(), 1)

        delete_all()
        self.assertEqual(Trade.query().count(), 0)
