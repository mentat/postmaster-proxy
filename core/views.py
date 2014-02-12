from core.jobs import check_stamps_authenticator
from core.models import CachedValues
from ext.handlers import BaseHandler
from ext.decorators import auth_required


class StampsAuthenticatorHandler(BaseHandler):
    """
    Provides the freshest authenticator available.
    """
    @auth_required
    def get(self):
        # First, check whether we have valid authenticator.
        # If not, it should get refreshed automatically.
        check_stamps_authenticator()
        # Now assuming that we DO have the freshest authenticator...
        obj = CachedValues.get_master()
        response = dict(
            production=obj.stamps_authenticator,
            testing=obj.stamps_authenticator_testing,
        )
        self.respond_json(response)
