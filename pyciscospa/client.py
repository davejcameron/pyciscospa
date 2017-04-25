"""PyCiscoSPA."""
from xml.etree.ElementTree import fromstring
import requests
from xmljson import parker

STATUS_URL = "http://{}/admin/status.xml&xuser={}&xpassword={}"
REBOOT_URL = 'http://{}/apply.cgi;session_id={}'


class PyCiscoSPAError(Exception):
    """Exception class for pyciscospa."""

    pass


class CiscoClient(object):
    """Cisco Phone Client."""

    def __init__(self, hostname, username='admin', password='admin'):
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

    def _get_session(self):
        """Get the current session id."""
        return self._data['router-status']['Session_ID']

    def phones(self):
        """Get the status of the phone lines."""
        self._get_data()
        status = self._data

        lines = []
        for line in [1, 2]:
            state = {
                'line':
                    line,
                'hook_state':
                    status['Hook_State_{}_'.format(line)],
                'call_duration':
                    status['Call_{}_Duration_1_'.format(line)],
                'call_peer_phone':
                    status['Call_{}_Peer_Phone_1_'.format(line)],
                'call_peer_name':
                    status['Call_{}_Peer_Name_1_'.format(line)],
                'call_state':
                    status['Call_{}_State_1_'.format(line)],
                'call_type':
                    status['Call_{}_Type_1_'.format(line)],
                'registration_state':
                    status['Registration_State'][line - 1],
                'last_called_number':
                    status['Last_Called_Number_{}_'.format(line)],
                'last_caller_number':
                    status['Last_Caller_Number_{}_'.format(line)],
                'last_registration_at':
                    status['Last_Registration_At'][line - 1],
                'next_registration':
                    status['Next_Registration_In'][line - 1],

            }

            lines.append(state)

        return lines

    def reboot(self):
        """Reboot the ATA."""
        self._get_data()

        payload = {'submit_button': 'Reboot',
                   'submit_type': '',
                   'change_action': '',
                   'gui_action': 'Apply',
                   'need_reboot': 1,
                   'session_key': self._get_session(),
                   'closeflg': 1,
                   'privilege_str': '',
                   'privilege_end': ''}

        raw_res = requests.post(REBOOT_URL.format(self.hostname,
                                                  self._get_session()),
                                data=payload)

        if raw_res.status_code == 200:
            return True
        return False
