# -*- coding: utf-8 -*-
"""
    stamps.services
    ~~~~~~~~~~~~~~~

    Stamps.com services.

    :copyright: 2012 by Jonathan Zempel.
    :license: BSD, see LICENSE for more details.
"""
from re import compile
import logging

from suds import WebFault
from suds.client import Client

from lib.future import Future


PATTERN_HEX = r"[0-9a-fA-F]"
PATTERN_ID = r"{hex}{{8}}-{hex}{{4}}-{hex}{{4}}-{hex}{{4}}-{hex}{{12}}".format(
    hex=PATTERN_HEX)
RE_TRANSACTION_ID = compile(PATTERN_ID)


class StampsException(Exception):
    def __init__(self, error):
        self.error_code = '0000'
        if hasattr(error.fault.detail, 'sdcerror'):
            if hasattr(error.fault.detail.sdcerror, '_code'):
                self.error_code = error.fault.detail.sdcerror._code
                self.value = error.fault.detail.sdcerror.value
            else:
                self.value = error.fault.detail.sdcerror
        else:
            self.value = error.message

    def __unicode__(self):
        return "%s (Error code: %s)" % (repr(self.value), self.error_code)

    def __str__(self):
        return self.__unicode__()


class StampsError(StampsException):
    pass


class BaseService(object):
    """Base service.

    :param configuration: API configuration.
    """

    def __init__(self, configuration):
        self.client = Client(configuration.wsdl)
        self.client.set_options(port=configuration.port)
        self.logger = logging.getLogger("stamps")
        self.logger.setLevel(logging.INFO)

    def call(self, method, **kwargs):
        """Call the given web service method.

        :param method: The name of the web service operation to call.
        :param kwargs: Method keyword-argument parameters.
        """
        self.logger.debug("%s(%s)", method, kwargs)
        instance = getattr(self.client.service, method)
        async = kwargs.get('__async', False)
        kwargs = dict((x,y) for x,y in kwargs.iteritems() if y is not None)

        def callback(future):
            try:
                ret_val = future.get_result()
            except WebFault as error:
                raise StampsError(error)

            return ret_val

        if async:
            return Future(instance(**kwargs), callback)
        else:
            try:
                ret_val = instance(**kwargs)
            except WebFault as error:
                raise StampsError(error)

            return ret_val

    def create(self, wsdl_type):
        """Create an object of the given WSDL type.

        :param wsdl_type: The WSDL type to create an object for.
        """
        return self.client.factory.create(wsdl_type)


class StampsService(BaseService):
    """Stamps.com service.
    """
    pass
