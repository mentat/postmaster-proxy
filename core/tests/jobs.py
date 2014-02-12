from mock import patch
from datetime import datetime, timedelta

from ext.utils import CloudTestCase

from core.jobs import refresh_stamps_authenticator, check_stamps_authenticator
from core.models import CachedValues
from lib.shipper.stamps import ExpiredAuthenticatorError

import settings


__all__ = [
    'RefreshStampsAuthenticatorTests',
    'CheckStampsAuthenticatorTests',
]


class RefreshStampsAuthenticatorTests(CloudTestCase):
    @patch('core.jobs.Stamps')
    def test_cooldown(self, m_stamps):
        obj = CachedValues.get_master()
        seconds = settings.STAMPS_REFRESH_COOLDOWN - 10
        then = datetime.now() - timedelta(seconds=seconds)
        obj.stamps_last_refresh = then
        obj.put()
        refresh_stamps_authenticator()
        self.assertEqual(m_stamps.call_count, 0)

    @patch('core.jobs.Stamps')
    def test_ok(self, m_stamps):
        obj = CachedValues.get_master()
        seconds = settings.STAMPS_REFRESH_COOLDOWN + 10
        m_stamps.return_value.refresh_authenticator.return_value = 'abc'
        then = datetime.now() - timedelta(seconds=seconds)
        obj.stamps_last_refresh = then
        obj.put()
        refresh_stamps_authenticator()
        self.assertEqual(m_stamps.call_count, 2)
        self.assertEqual(m_stamps().refresh_authenticator.call_count, 2)
        obj = CachedValues.get_master()
        self.assertEqual(obj.stamps_authenticator, 'abc')
        self.assertEqual(obj.stamps_authenticator_testing, 'abc')
        self.assertGreater(obj.stamps_last_refresh, then)


class CheckStampsAuthenticatorTests(CloudTestCase):
    @patch('core.jobs.Stamps')
    def test_ok(self, m_stamps):
        check_stamps_authenticator()
        self.assertEqual(m_stamps.call_count, 2)
        self.assertEqual(m_stamps().sample_request.call_count, 2)

    @patch('core.jobs.refresh_stamps_authenticator')
    @patch('core.jobs.Stamps')
    def test_exception(self, m_stamps, m_refresh):
        m_stamps().sample_request.side_effect = ExpiredAuthenticatorError
        check_stamps_authenticator()
        m_refresh.assert_called_with()
