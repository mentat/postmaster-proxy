from mock import patch

from ext.utils import CloudTestCase

from core.cron import app as cron_app


__all__ = [
    'RefreshStampsAuthenticatorCronTests',
]


class RefreshStampsAuthenticatorCronTests(CloudTestCase):
    APP = cron_app

    @patch('core.cron.refresh_stamps_authenticator')
    def test_get(self, m_r):
        self.app.get('/cron/refresh_stamps_authenticator')
        m_r.assert_called_with()
