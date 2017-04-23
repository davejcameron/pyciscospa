# -*- coding: utf-8 -*-
"""Command line interface."""
from __future__ import print_function

import argparse
import sys

from pyciscospa import CiscoClient


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host',
                        required=True, help='SPA* host')
    parser.add_argument('-u', '--username',
                        required=False, default='admin', help='SPA* username')
    parser.add_argument('-p', '--password',
                        required=False, default='admin', help='Password')
    parser.add_argument('-r', '--reboot', action='store_true',
                        default=False, help='Reboot SPA')
    args = parser.parse_args()

    client = CiscoClient(args.host, args.username, args.password)

    if args.reboot:
        client.reboot()
    else:
        print(client.phones())


if __name__ == '__main__':
    sys.exit(main())
