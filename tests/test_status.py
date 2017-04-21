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
    def test_valid_username_password_returns_list(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        self.assertIsInstance(client.get_phones(), list)

    @requests_mock.Mocker()
    def test_get_phones_returns_list(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        phone_lines = [{'registration_state': 'Registered',
                        'state': 'Idle',
                        'last_caller_number': 18007773333,
                        'hook_state': 'On',
                        'line': 1,
                        'next_registration': '55 s',
                        'last_called_number': 15555555555,
                        'last_registration_at': '4/20/2017 14:17:53'},
                       {'registration_state': 'Registered',
                        'state': 'Idle',
                        'last_caller_number': None,
                        'hook_state': 'On',
                        'line': 2,
                        'next_registration': '202 s',
                        'last_called_number': None,
                        'last_registration_at': '4/20/2017 14:13:45'}]
        self.assertListEqual(client.get_phones(), phone_lines)

    @requests_mock.Mocker()
    def test_get_phones_should_return_None(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1', 'admin', 'admin')
        self.assertEqual(client.get_phones()[1]['last_called_number'], None)
