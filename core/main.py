from webapp2 import Route, WSGIApplication

from ext.helpers import fix_path; fix_path()

import views


app = WSGIApplication([
    # Views
    Route('/stamps_authenticator', views.StampsAuthenticatorHandler),
], debug=True)
