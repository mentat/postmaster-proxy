import logging

from ext.helpers import fix_path; fix_path()

from core.models import CachedValues
from lib.shipper import Stamps


def refresh_stamps_authenticator():
    obj = CachedValues.get_master()
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
