import unittest
import requests
import requests_mock
from pyciscospa.client import CiscoClient, PyCiscoSPAError
from tests.common import load_fixture


class TestGetPhones(unittest.TestCase):

    @requests_mock.Mocker()
    def test_invalid_username_password_raises_exception(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=username&xpassword'
                 '=password', status_code=401)
        client = CiscoClient('127.0.0.1', 'username', 'password')
        self.assertRaises(PyCiscoSPAError, client.get_phones)

    @requests_mock.Mocker()
    def test_invalid_hostname_raises_exception(self, mock):
        mock.get('http://127.0.0.2/admin/status.xml&xuser=username&xpassword'
                 '=password', exc=requests.exceptions.ConnectTimeout)
        client = CiscoClient('127.0.0.2', 'username', 'password')
        self.assertRaises(requests.exceptions.ConnectionError,
                          client.get_phones)

    @requests_mock.Mocker()
    def test_valid_username_password(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        self.assertIsInstance(client.get_phones(), list)
