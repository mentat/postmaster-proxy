from datetime import datetime, timedelta
import logging

from ext.helpers import fix_path; fix_path()

from core.models import CachedValues
from lib.shipper import Stamps
from lib.shipper.stamps import ExpiredAuthenticatorError

import settings


def refresh_stamps_authenticator():
    """
    Refreshes Stamps authenticator for production and testing server,
    and stores it in the Datastore.
    """
    obj = CachedValues.get_master()
    # First, check whether last refresh didn't happen recently
    delta = timedelta(seconds=settings.STAMPS_REFRESH_COOLDOWN)
    cooldown = (
        obj.stamps_last_refresh + delta
        if obj.stamps_last_refresh else datetime.now() + delta
    )
    if cooldown > datetime.now():
        return
    obj.stamps_last_refresh = datetime.now()
    # It will be cached in memcache anyway
    obj.put()
    # Production
    logging.info('Refreshing Stamps authenticator for production server')
    stamps = Stamps(testing=False)
    authenticator = stamps.refresh_authenticator()
    obj.stamps_authenticator = authenticator
    # Testing
    logging.info('Refreshing Stamps authenticator for testing server')
    stamps = Stamps(testing=True)
    authenticator = stamps.refresh_authenticator()
    obj.stamps_authenticator_testing = authenticator
    logging.info('Refreshing successful')
    obj.put()


def check_stamps_authenticator():
    """
    Checks whether current Stamps authenticators are valid.
    In case any of them is found invalid, both of them are refreshed.
    """
    try:
        # First, production.
        logging.info('Checking Stamps production authenticator.')
        stamps = Stamps(testing=False)
        stamps.sample_request()
        # Then, testing!
        logging.info('Checking Stamps testing authenticator.')
        stamps = Stamps(testing=True)
        stamps.sample_request()
    except ExpiredAuthenticatorError:
        # Uh oh! Better try to refresh now!
        logging.info('Stamps production authenticator expired! Refreshing now.')
        # We're not deferring this, because it needs to be refreshed in the
        # same request in order to provide it to user.
        refresh_stamps_authenticator()
