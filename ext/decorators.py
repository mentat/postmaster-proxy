import logging

import settings


def auth_required(handler):
    def wrapped(self, *args, **kwargs):
        try:
            token = self.request.headers.get('X-PM-Auth', '')
        except Exception:
            raise self.abort(401)
        if token != settings.SECRET_KEY:
            self.abort(401)
        else:
            msg = 'Request from %s authorized' % self.request.remote_addr
            logging.info(msg)
            return handler(self, *args, **kwargs)
    return wrapped
