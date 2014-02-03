from webapp2 import Route, WSGIApplication

from ext.handlers import BaseHandler
from ext.helpers import fix_path; fix_path()

from core.jobs import refresh_stamps_authenticator


class RefreshStampsAuthenticator(BaseHandler):
    """
    Periodically and forcefully refreshes Stamps authenticator.
    """
    def get(self):
        refresh_stamps_authenticator()


app = WSGIApplication([
    Route('/cron/refresh_stamps_authenticator', RefreshStampsAuthenticator),
], debug=True)
