import logging

import settings


__all__ = [
    'auth_required'
]


def auth_required(handler):
    """
    Checks for X-PM-Auth header in incoming request, and compares it to the
    value stored in settings.
    """
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
