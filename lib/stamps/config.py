# -*- coding: utf-8 -*-
"""
    stamps.config
    ~~~~~~~~~~~~~

    Stamps.com configuration.

    :copyright: 2012 by Jonathan Zempel.
    :license: BSD, see LICENSE for more details.
"""
import logging
import os


class StampsConfiguration(object):
    """Stamps service configuration.

    :param integration_id: Unique ID, provided by Stamps.com,
        that represents your application.
    :param username: Stamps.com account username.
    :param password: Stamps.com password.
    :param testing: Default `False`.
    :param authenticator: Stamps Authenticator. Used in requests.
    """

    def __init__(self, integration_id, username, password, testing=False):

        self.integration_id = integration_id
        self.username = username
        self.password = password
        self.testing = testing

        file_path = os.path.abspath(__file__)
        directory_path = os.path.dirname(file_path)

        if testing:
            logging.info('Using test server')
            file_name = "stamps_v34.test.wsdl"
        else:
            logging.info('Using production server')
            file_name = "stamps_v34.wsdl"

        wsdl = os.path.join(directory_path, "wsdls", file_name)
        self.wsdl = "file://{0}".format(wsdl)

        self.port = "SwsimV34Soap12"

        assert self.integration_id
        assert self.username
        assert self.password
        assert self.wsdl
        assert self.port
