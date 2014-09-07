import json

import webapp2

from models import Trade


class Handler(webapp2.RequestHandler):

    def get(self):
        """
        Returns a JSON containing the Trades in the system.
        Fields returned are filtered by the get parameter 'f'.
        Trades are filtered by timestamp:
            'timestamp_gt': All the trades with a timestamp greater than
            'timestamp_lt': All the trades with a timestamp lesser than
        """
        self.response.headers['Content-Type'] = 'application/json'
        fields = self.request.GET.get('f')
        timestamp_gt = self.request.GET.get('timestamp_gt')
        timestamp_lt = self.request.GET.get('timestamp_lt')
        fields = fields.split(',') if fields else None

        result = Trade.query_by_timestamp(timestamp_lt, timestamp_gt)

        data = [trade.serialize(fields=fields) for trade in result]
        self.response.write(json.dumps(data, indent=4))

application = webapp2.WSGIApplication([
    ('/', Handler),
], debug=True)
