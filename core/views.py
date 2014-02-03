from core.models import CachedValues
from ext.handlers import BaseHandler


class StampsAuthenticatorHandler(BaseHandler):
    """
    """
    def get(self):
        obj = CachedValues.get_master()
        response = dict(
            production=obj.stamps_authenticator,
            testing=obj.stamps_authenticator_testing,
        )
        self.respond_json(response)
