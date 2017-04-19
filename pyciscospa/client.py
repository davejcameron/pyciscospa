"""
PyCiscoSPA
"""
from lxml.etree import fromstring
from xmljson import yahoo
from json import dumps

import pprint
import requests

STATUS_URL = "http://{}/admin/status.xml&xuser={}&xpassword={}"


class Phone(object):
    def __init__(self, dictionary):
        self.state = None
        self.hook_state = None
        self.last_called_number = None
        self.last_caller_number = None
        self.last_registration_at = None
        self.registration_state = None
        self.next_registration = None

        for k, v in dictionary.items():
            setattr(self, k, v)

    def to_json(self):
        return dumps(self.__dict__)


class PyCiscoSPAError(Exception):
    pass


class CiscoClient(object):

    def __init__(self, hostname, username, password):
        """Initialize the client object."""
        self.username = username
        self.password = password
        self._data = {}

    def _get_data(self):
        """Gets the status from the phone system"""

        raw_res = requests.get(STATUS_URL.format('192.168.1.16',self.username, self.password))
        self._data = yahoo.data(fromstring(raw_res.content))

    def get_phones(self):
        self._get_data()
        status = self._data['flat-status']
        pprint.pprint(self._data)
        for line_number in [1,2]:
            line_state = {'state': status['Call_{}_State_1_'.format(line_number)],
                          'hook_state': status['Hook_State_{}_'.format(line_number)],
                          'registration_state': status['Registration_State'][line_number-1],
                          'last_called_number': status['Last_Called_Number_{}_'.format(line_number)],
                          'last_caller_number': status['Last_Caller_Number_{}_'.format(line_number)],
                          'last_registration_at': status['Last_Registration_At'][line_number - 1],
                          'next_registration': status['Next_Registration_In'][line_number-1]
                          }
            phone = Phone(line_state)
            print(phone.to_json())


