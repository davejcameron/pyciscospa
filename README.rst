Cisco SPA ATA devices |Build Status| |PyPi Version|
===================================================

A library to interact with the SPA112 ATA to gather phone line status details and reboot the device remotely.


Command Line Usage
------------------

1. Install PyCiscoSPA.

   .. code:: python

      pip install pyciscospa

2. Get the status of the connected phone lines (default admin/admin)

   .. code:: bash

      pyciscospa --host 192.168.1.20
      pyciscospa --host 192.168.1.20 -u admin -p admin

3. Reboot the ATA

   .. code:: bash

      pyciscospa --host 192.168.1.20 --reboot
      pyciscospa --host 192.168.1.20 -u admin -p admin --reboot


Module Usage
------------

1. Get phone lines status

   .. code:: python

      from pyciscospa import CiscoClient

      client = CiscoClient(192.168.1.20)
      phone_lines = client.phones()

2. Reboot the ATA

   .. code:: python

      from pyciscospa import CiscoClient

      client = CiscoClient(192.168.1.20)
      client.reboot()




.. |Build Status| image:: https://travis-ci.org/davejcameron/pyciscospa.svg?branch=master
   :target: https://travis-ci.org/davejcameron/pyciscospa

.. |PyPi Version| image:: https://img.shields.io/pypi/v/pyciscospa.svg
   :target: https://pypi.python.org/pypi/pyciscospa/