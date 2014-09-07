from google.appengine.ext import ndb

from utils import parse_timestamp


class Trade(ndb.Model):
    """
    Model representing a Trade in the NDB Datastore
    """
    date = ndb.DateProperty()
    symbol = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()
    timestamp_nanoseconds = ndb.IntegerProperty()
    quotecount = ndb.IntegerProperty()
    tradecount = ndb.IntegerProperty()
    openpx = ndb.FloatProperty()
    closepx = ndb.FloatProperty()
    highpx = ndb.FloatProperty()
    lowpx = ndb.FloatProperty()

    def get_field(self, field):
        """
        Returns the field of the Trade or its isoformat if it
        is a date or a datetime
        """
        if field == 'timestamp':
            zeros = '0' * (9 - len(str(self.timestamp_nanoseconds)))
            return "{}.{}{}".format(
                self.timestamp, zeros, self.timestamp_nanoseconds)
        elif field == 'date':
            return self.date.isoformat()
        else:
            return getattr(self, field)

    def serialize(self, fields=None):
        """
        Serialize the selected fields values so that
        they can be dumped in a JSON
        """
        if fields is None:
            keys = Trade._properties.keys()
            keys.remove('timestamp_nanoseconds')
            fields = keys

        return {field: self.get_field(field) for field in fields}

    @staticmethod
    def query_by_timestamp(timestamp_lt, timestamp_gt):
        """
        Returns all the Trades within the "less than" and "greater than"
        timestamps
        """
        query = Trade.query()
        if timestamp_lt is not None:
            timestamp_lt, nanoseconds_lt = parse_timestamp(timestamp_lt)
            query = query.filter(
                ndb.OR(
                    Trade.timestamp < timestamp_lt,
                    ndb.AND(
                        Trade.timestamp == timestamp_lt,
                        Trade.timestamp_nanoseconds < nanoseconds_lt
                    )
                )
            )

        second_query = None
        if timestamp_gt is not None:
            timestamp_gt, nanoseconds_gt = parse_timestamp(timestamp_gt)
            args = [
                ndb.OR(
                    Trade.timestamp > timestamp_gt,
                    ndb.AND(
                        Trade.timestamp == timestamp_gt,
                        Trade.timestamp_nanoseconds > nanoseconds_gt
                    )
                )
            ]
            if timestamp_lt is None:
                query = query.filter(*args)
            else:
                second_query = Trade.query(*args)

        if second_query is None:
            return query
        else:
            # The Datastore rejects queries using inequality filtering
            # on more than one property. Therefore we need to evaluate
            # the diff between the two queries manually
            query_keys = [x for x in query.iter(keys_only=True)]
            second_query_keys = [x for x in second_query.iter(keys_only=True)]
            shared_keys = set(query_keys) & set(second_query_keys)
            return Trade.query(Trade.key.IN(shared_keys))
