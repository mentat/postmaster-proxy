from mock import patch
import json

from ext.utils import CloudTestCase

from core.main import app as main_app


__all__ = [
    'StampsAuthenticatorHandlerTests',
]


class StampsAuthenticatorHandlerTests(CloudTestCase):
    APP = main_app

    def test_auth(self):
        self.app.get('/stamps_authenticator', status=401)

    @patch('core.views.check_stamps_authenticator')
    def test_check(self, m_c):
        self.auth_get('/stamps_authenticator')
        m_c.assert_called_with()

    @patch('core.views.check_stamps_authenticator')
    def test_response(self, m_c):
        raw = self.auth_get('/stamps_authenticator')
        resp = json.loads(raw.body)
        self.assertIn('production', resp)
        self.assertIn('testing', resp)
