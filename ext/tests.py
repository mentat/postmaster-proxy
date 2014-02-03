from mock import MagicMock, patch
import unittest

from ext.decorators import auth_required

__all__ = [
    'DecoratorsTestCase'
]


class DecoratorsTestCase(unittest.TestCase):
    def test_auth_required_exception(self):
        h_self = MagicMock()
        wrap = auth_required(None)
        h_self.abort.side_effect = ValueError
        with self.assertRaises(ValueError):
            wrap(h_self)
        h_self.abort.assert_called_with(401)

    @patch('ext.decorators.settings')
    def test_auth_required_invalid_token(self, m_s):
        h_self = MagicMock()
        wrap = auth_required(None)
        h_self.request.headers.get.return_value = 'abc'
        m_s.SECRET_KEY = 'def'
        h_self.abort.side_effect = ValueError
        with self.assertRaises(ValueError):
            wrap(h_self)
        h_self.abort.assert_called_with(401)

    @patch('ext.decorators.settings')
    def test_auth_required(self, m_s):
        handler = MagicMock()
        h_self = MagicMock()
        wrap = auth_required(handler)
        h_self.request.headers.get.return_value = 'abc'
        m_s.SECRET_KEY = 'abc'
        result = wrap(h_self)
        handler.assert_called_with(h_self)
        self.assertEqual(result, handler())
