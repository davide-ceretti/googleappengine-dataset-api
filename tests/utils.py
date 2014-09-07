import unittest

import webtest

from google.appengine.ext import testbed

from api import application


class NDBTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.testapp = webtest.TestApp(application)

    def tearDown(self):
        self.testbed.deactivate()
