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
        self.assertRaises(PyCiscoSPAError, client.phones)

    @requests_mock.Mocker()
    def test_invalid_hostname_raises_exception(self, mock):
        mock.get('http://127.0.0.2/admin/status.xml&xuser=username&xpassword'
                 '=password', exc=requests.exceptions.ConnectTimeout)
        client = CiscoClient('127.0.0.2', 'username', 'password')
        self.assertRaises(requests.exceptions.ConnectionError,
                          client.phones)

    @requests_mock.Mocker()
    def test_valid_username_password_returns_list(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        self.assertIsInstance(client.phones(), list)

    @requests_mock.Mocker()
    def test_phones_returns_dictionary(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        line_1 = client.phones()[0]
        self.assertEqual(line_1['registration_state'], 'Registered')
        self.assertEqual(line_1['call_duration'], None)
        self.assertEqual(line_1['call_peer_phone'], None)
        self.assertEqual(line_1['call_peer_name'], None)
        self.assertEqual(line_1['call_state'], 'Idle')
        self.assertEqual(line_1['call_type'], None)
        self.assertEqual(line_1['last_caller_number'], 18007773333)
        self.assertEqual(line_1['last_called_number'], 15555555555)
        self.assertEqual(line_1['last_registration_at'], '4/20/2017 14:17:53')
        self.assertEqual(line_1['line'], 1)
        self.assertEqual(line_1['next_registration'], '55 s')

    @requests_mock.Mocker()
    def test_phones_should_return_None(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        self.assertEqual(client.phones()[1]['last_called_number'], None)
