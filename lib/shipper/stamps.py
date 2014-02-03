from core.models import CachedValues
from lib.stamps.config import StampsConfiguration
from lib.stamps.services import StampsService, StampsError


import settings


class ExpiredAuthenticatorError(Exception):
    pass


class Stamps(object):
    ERROR_CODES = (
        '002B0202', # Expired authenticator
        '002B0203', # Invalid conversation token
        '002B0204', # Conversation out of sync
    )

    def __init__(self, testing=False):
        if testing:
            s = settings.CARRIERS_TEST
        else:
            s = settings.CARRIERS_LIVE
        STAMPS = s['stamps']

        self.config = StampsConfiguration(
            STAMPS['integration_id'],
            STAMPS['username'],
            STAMPS['password'],
            testing=testing,
        )
        self.service = StampsService(self.config)

    def sample_request(self):
        obj = CachedValues.get_master()
        authenticator = (
            obj.stamps_authenticator_testing
            if self.config.testing else obj.stamps_authenticator
        )
        try:
            self.service.call(
                'GetSupportedCountries',
                Authenticator=authenticator,
            )
        except StampsError as e:
            if e.error_code in self.ERROR_CODES:
                raise ExpiredAuthenticatorError
            else:
                raise

    def refresh_authenticator(self):
        """
        Used by cron job. Returns new Stamps authenticator.
        """
        credentials = self.service.create('Credentials')
        credentials.IntegrationID = self.config.integration_id
        credentials.Username = self.config.username
        credentials.Password = self.config.password
        response = self.service.call(
            'AuthenticateUser',
            Credentials=credentials
        )
        return response.Authenticator
