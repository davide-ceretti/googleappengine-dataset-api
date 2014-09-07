import datetime
import json

from models import Trade
from tests.utils import NDBTestCase


class TestAPI(NDBTestCase):

    def test_get_200(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)

    def create_trade(self, **custom_kwargs):
        kwargs = {
            'date': datetime.date(2014, 1, 1),
            'symbol': 'SYM',
            'timestamp': datetime.datetime(2014, 1, 1, 14, 52, 11),
            'timestamp_nanoseconds': 10142,
            'quotecount': 15,
            'tradecount': 16,
            'openpx': 10.12,
            'closepx': 10.13,
            'highpx': 21.5,
            'lowpx': 22,
        }
        if custom_kwargs:
            kwargs.update(custom_kwargs)

        Trade(**kwargs).put()

    def test_content_type(self):
        response = self.testapp.get('/')
        self.assertEqual(response.content_type, 'application/json')

    def test_content_empty_datastore(self):
        response = self.testapp.get('/')
        self.assertEqual(response.normal_body, '[]')

    def test_content_one_trade(self):
        self.create_trade()

        response = self.testapp.get('/')

        expected = [
            {
                'date': '2014-01-01',
                'symbol': 'SYM',
                'timestamp': '2014-01-01 14:52:11.000010142',
                'quotecount': 15,
                'tradecount': 16,
                'highpx': 21.5,
                'closepx': 10.13,
                'openpx': 10.12,
                'lowpx': 22.0,
            }
        ]
        self.assertEqual(response.status_int, 200)
        self.assertEqual(json.loads(response.normal_body), expected)

    def test_one_field(self):
        self.create_trade(symbol='ABCD')

        response = self.testapp.get('/?f=symbol')
        expected = [
            {
                'symbol': 'ABCD',
            }
        ]
        self.assertEqual(response.status_int, 200)
        self.assertEqual(json.loads(response.normal_body), expected)

    def test_multiple_fields(self):
        self.create_trade(symbol='ABCD', highpx=100)

        response = self.testapp.get('/?f=symbol,highpx')
        expected = [
            {
                'symbol': 'ABCD',
                'highpx': 100,
            }
        ]
        self.assertEqual(response.status_int, 200)
        self.assertEqual(json.loads(response.normal_body), expected)

    def test_timestamp_lt(self):
        self.create_trade(
            symbol='0',
            timestamp=datetime.datetime(2013, 12, 31, 23, 59, 59),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='1',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 0),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='2',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 1),
            timestamp_nanoseconds=0,
        )

        url = '/?f=symbol&timestamp_lt=2014-01-01 00:00:01.000000000'
        response = self.testapp.get(url)
        expected = [
            {
                'symbol': '0',
            },
            {
                'symbol': '1',
            },
        ]
        self.assertEqual(response.status_int, 200)
        self.assertEqual(json.loads(response.normal_body), expected)

    def test_timestamp_gt(self):
        self.create_trade(
            symbol='0',
            timestamp=datetime.datetime(2013, 12, 31, 23, 59, 59),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='1',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 0),
            timestamp_nanoseconds=999999998,
        )

        self.create_trade(
            symbol='2',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 0),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='3',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 1),
            timestamp_nanoseconds=0,
        )

        url = '/?f=symbol&timestamp_gt=2014-01-01 00:00:00.999999998'
        response = self.testapp.get(url)
        expected = [
            {
                'symbol': '2',
            },
            {
                'symbol': '3',
            },
        ]
        expected.sort()
        self.assertEqual(response.status_int, 200)
        self.assertEqual(sorted(json.loads(response.normal_body)), expected)

    def test_timestamp_lt_and_gt(self):
        self.create_trade(
            symbol='0',
            timestamp=datetime.datetime(2013, 12, 31, 23, 59, 59),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='1',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 0),
            timestamp_nanoseconds=999999999,
        )

        self.create_trade(
            symbol='2',
            timestamp=datetime.datetime(2014, 1, 1, 0, 0, 1),
            timestamp_nanoseconds=0,
        )

        gt = 'timestamp_gt=2014-01-01 00:00:00.999999998'
        lt = 'timestamp_lt=2014-01-01 00:00:01.000000000'
        url = '/?f=symbol&{}&{}'.format(lt, gt)
        response = self.testapp.get(url)
        expected = [
            {
                'symbol': '1',
            },
        ]
        self.assertEqual(response.status_int, 200)
        self.assertEqual(json.loads(response.normal_body), expected)
