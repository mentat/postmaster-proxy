from lib.stamps.config import StampsConfiguration
from lib.stamps.services import StampsService

import settings


class Stamps(object):
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
