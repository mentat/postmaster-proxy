import settings


def auth_required(handler):
    def wrapped(self, *args, **kwargs):
        try:
            partner, token = self.request.headers.get('X-PM-Auth', '')
        except Exception:
            raise self.abort(401)
        if token != settings.SECRET_KEY:
            self.abort(401)
        else:
            return handler(self, *args, **kwargs)
    return wrapped