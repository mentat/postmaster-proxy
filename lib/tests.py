from mock import MagicMock, patch

from ext.utils import CloudTestCase

from core.models import CachedValues
from lib.shipper import Stamps


class StampsTestCase(CloudTestCase):
    @patch('lib.shipper.stamps.settings')
    @patch('lib.shipper.stamps.StampsService')
    def test_init_testing(self, m_service, m_s):
        m_s.CARRIERS_TEST = dict(
            stamps=dict(
                integration_id=123,
                username='abc',
                password='def'
            )
        )
        stamps = Stamps(testing=True)
        self.assertEqual(stamps.config.integration_id, 123)
        self.assertEqual(stamps.config.username, 'abc')
        self.assertEqual(stamps.config.password, 'def')
        self.assertEqual(stamps.config.testing, True)
        m_service.assert_called_with(stamps.config)

    @patch('lib.shipper.stamps.settings')
    @patch('lib.shipper.stamps.StampsService')
    def test_init_production(self, m_service, m_s):
        m_s.CARRIERS_LIVE = dict(
            stamps=dict(
                integration_id=123,
                username='abc',
                password='def'
            )
        )
        stamps = Stamps(testing=False)
        self.assertEqual(stamps.config.integration_id, 123)
        self.assertEqual(stamps.config.username, 'abc')
        self.assertEqual(stamps.config.password, 'def')
        self.assertEqual(stamps.config.testing, False)
        m_service.assert_called_with(stamps.config)

    @patch('lib.shipper.stamps.settings')
    @patch('lib.shipper.stamps.StampsService')
    def test_refresh_authenticator(self, m_service, m_s):
        m_s.CARRIERS_LIVE = dict(
            stamps=dict(
                integration_id=123,
                username='abc',
                password='def'
            )
        )
        creds = MagicMock()
        m_service().create.return_value = creds
        stamps = Stamps(testing=False)
        stamps.refresh_authenticator()
        m_service().call.assert_called_with(
            'AuthenticateUser', Credentials=creds
        )
        self.assertEqual(creds.IntegrationID, 123)
        self.assertEqual(creds.Username, 'abc')
        self.assertEqual(creds.Password, 'def')

    @patch('lib.shipper.stamps.StampsService')
    def test_sample_request(self, m_s):
        obj = CachedValues.get_master()
        obj.stamps_authenticator = 'abcde'
        obj.put()
        stamps = Stamps(testing=False)
        stamps.sample_request()
        m_s().call.assert_called_with(
            'EnumCostCodes', Authenticator='abcde'
        )

    @patch('lib.shipper.stamps.StampsService')
    def test_sample_request_testing(self, m_s):
        obj = CachedValues.get_master()
        obj.stamps_authenticator = 'abcde'
        obj.stamps_authenticator_testing = 'ghijk'
        obj.put()
        stamps = Stamps(testing=True)
        stamps.sample_request()
        m_s().call.assert_called_with(
            'EnumCostCodes', Authenticator='ghijk'
        )

    @patch('lib.shipper.stamps.StampsService')
    def test_sample_request_error(self, m_s):
        from lib.shipper.stamps import ExpiredAuthenticatorError
        from lib.stamps.services import StampsError
        obj = CachedValues.get_master()
        obj.stamps_authenticator = 'abcde'
        obj.put()
        error = StampsError(MagicMock())
        error.error_code = '002B0202'
        m_s().call.side_effect = error
        stamps = Stamps(testing=False)
        with self.assertRaises(ExpiredAuthenticatorError):
            stamps.sample_request()

    @patch('lib.shipper.stamps.StampsService')
    def test_sample_request_error_other(self, m_s):
        from lib.stamps.services import StampsError
        obj = CachedValues.get_master()
        obj.stamps_authenticator = 'abcde'
        obj.put()
        error = StampsError(MagicMock())
        error.error_code = 'ABCDE'
        m_s().call.side_effect = error
        stamps = Stamps(testing=False)
        with self.assertRaises(StampsError):
            stamps.sample_request()
