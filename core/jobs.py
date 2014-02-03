from ext.helpers import fix_path; fix_path()

from core.models import CachedValues
from lib.shipper import Stamps


def refresh_stamps_authenticator():
    obj = CachedValues.get_master()
    # Production
    stamps = Stamps(testing=False)
    authenticator = stamps.refresh_authenticator()
    obj.stamps_authenticator = authenticator
    # Testing
    stamps = Stamps(testing=True)
    authenticator = stamps.refresh_authenticator()
    obj.stamps_authenticator_testing = authenticator
    obj.put()
