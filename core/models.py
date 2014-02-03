from google.appengine.ext import ndb


class CachedValues(ndb.Model):
    """
    Base singleton entity to store all kinds of values.
    """
    stamps_authenticator = ndb.StringProperty(indexed=False)
    stamps_authenticator_testing = ndb.StringProperty(indexed=False)
    stamps_last_refresh = ndb.DateTimeProperty()

    @classmethod
    def get_master(cls):
        return cls.get_or_insert('master', namespace='')
