import unittest

import requests_mock
from pyciscospa.client import CiscoClient
from tests.common import load_fixture


class TestReboot(unittest.TestCase):
    @requests_mock.Mocker()
    def test_get_session_id(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        client = CiscoClient('127.0.0.1')
        client._get_data()
        self.assertEqual(client._get_session(),
                         '9af6437ca20821d021fb71c2a5197922')

    @requests_mock.Mocker()
    def test_reboot(self, mock):
        mock.get('http://127.0.0.1/admin/status.xml&xuser=admin&xpassword'
                 '=admin', text=load_fixture("status_registered.xml"))
        mock.post(
            'http://127.0.0.1/apply.cgi;session_id='
            '9af6437ca20821d021fb71c2a5197922',
            status_code=200)
        client = CiscoClient('127.0.0.1')
        self.assertEquals(client.reboot(), True)
