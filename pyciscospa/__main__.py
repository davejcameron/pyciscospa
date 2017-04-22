# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import sys

from pyciscospa import CiscoClient


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host',
                        required=True, help='SPA* host')
    parser.add_argument('-u', '--username',
                        required=True, help='SPA* username')
    parser.add_argument('-p', '--password',
                        required=True, help='Password')
    parser.add_argument('-j', '--json', action='store_true',
                        default=False, help='Json output')
    args = parser.parse_args()

    client = CiscoClient(args.host, args.username, args.password)

    print(client.get_phones())


if __name__ == '__main__':
    sys.exit(main())
