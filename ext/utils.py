import webtest
import unittest
import os

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
from google.appengine.api.search import simple_search_stub
from webapp2 import Request

import settings


__all__ = [
    'CloudTestCase'
]


class CloudTestCase(unittest.TestCase):
    APP = None

    _EXISTING_EMAILS = []

    def setUp(self):
        # To avoid issues with the app_identity service in settings.py.
        os.environ['DEFAULT_VERSION_HOSTNAME'] = 'testing'

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_files_stub()
        self.testbed.init_app_identity_stub()
        search_stub = simple_search_stub.SearchServiceStub()
        self.testbed._register_stub('search', search_stub)
        self._current_tasks = {}

        # We're importing the apps here to avoid importing settings.py
        # before the app_identity stub is initialized.
        if not self.APP:
            from core.main import app as main_app
            self.APP = main_app
        elif isinstance(self.APP, str):
            module = __import__(self.APP)
            self.APP = module.main.app
        request = Request.blank('/')
        request.app = self.APP
        self.APP.set_globals(request=request)
        self.app = webtest.TestApp(self.APP)

    def tearDown(self):
        self.testbed.deactivate()
        del os.environ['DEFAULT_VERSION_HOSTNAME']

    def auth_get(self, *args, **kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['X-PM-Auth'] = settings.SECRET_KEY
        return self.app.get(*args, **kwargs)
