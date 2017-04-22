"""PyCiscoSPA."""
import requests
from lxml.etree import fromstring
from xmljson import parker

STATUS_URL = "http://{}/admin/status.xml&xuser={}&xpassword={}"


class PyCiscoSPAError(Exception):
    """Exception class for pyciscospa."""

    pass


class CiscoClient(object):
    """Cisco Phone Client."""

    def __init__(self, hostname, username, password):
        """Initialize the client object."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self._data = {}

    def _get_data(self):
        """Get the status from the phone system."""
        raw_res = requests.get(STATUS_URL.format(self.hostname, self.username,
                                                 self.password))

        if not raw_res.status_code == 200:
            raise PyCiscoSPAError("Login Error: Bad HTTP status code.")
        self._data = parker.data(fromstring(raw_res.content))

    def get_phones(self):
        """Get the status of the phone lines."""
        self._get_data()
        status = self._data

        lines = []
        for line in [1, 2]:
            state = {
                'line':
                    line,
                'state':
                    status['Call_{}_State_1_'.format(line)],
                'hook_state':
                    status['Hook_State_{}_'.format(line)],
                'registration_state':
                    status['Registration_State'][line - 1],
                'last_called_number':
                    status['Last_Called_Number_{}_'.format(line)],
                'last_caller_number':
                    status['Last_Caller_Number_{}_'.format(line)],
                'last_registration_at':
                    status['Last_Registration_At'][line - 1],
                'next_registration':
                    status['Next_Registration_In'][line - 1]
            }

            lines.append(state)

        return lines
