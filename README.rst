.. image:: https://img.shields.io/:license-mit-blue.svg
    :target: http://doge.mit-license.org
    :align: left
    
.. image:: https://badge.fury.io/py/py-momit-cool-remote.svg
    :target: https://pypi.python.org/pypi/py-momit-cool-remote

.. image:: http://alphaclima.gr/store/wp-content/uploads/2017/03/momit-cool-logo.jpg

``py-momit-cool-remote`` is a Python 3 library for remotely controlling your air conditioning unit through the use of the Momit Cool.

The Momit Cool is a small device that can be attached to your AC, allowing you to control it from your smart phone. In order to accomplish remote control from anywhere, commands are sent to their central server, which then sends them to your Momit Gateway device. ``py-momit-cool-remote`` communicates directly with the Momit Gateway, completely circumventing Momit's servers.

https://www.momit.com/en-ro/products/cool

Note: Python 3.5 and newer only.

Installation
------------

.. code-block:: bash

    $ pip install py-momit-cool-remote

Make sure that ``pip`` refers to the ``pip`` installation for Python 3. You might have to install the package using ``pip3``.

Example usage
-------------

.. code-block:: python

    from momitcool import MomitCool

    cool = MomitCool('192.168.3.164')
    cool.cool() # turn on in cooling mode
    cool.off() # turn off
    cool.temperature() # get current temperature
    cool.mode() # cooling/heating/off

.. code-block:: bash

    $ momit-cool --host 192.168.3.164 --cool
    $ momit-cool --host 192.168.3.164 --off
    $ momit-cool --host 192.168.3.164 --temperature
    $ momit-cool --host 192.168.3.164 --mode

Details
-------
The Momit Cool is a commercial, closed source product that does not have any documentation on how communication is performed. All of the information provided in this repository was found by reverse engineering the protocol. I uncovered most of the information by ARP poisoning and intercepting the traffic between the Momit Gateway and the Momit servers. The Momit Gateway communicates over the CoAP protocol.

CoAP servers typically implement the CoRE standard, allowing service and resource discovery. Performing this on the Momit Cool Gateway allows us to retrieve a list of available resources:

.. code-block::

    coap get coap://192.168.3.164:11686/.well-known/core

    </.well-known/core>;ct=40,
    <//>;title="Default root resource",
    </0/1>;title="Security: PUT value";rt="Security",
    </1/1>;title="Server: PUT value";rt="Server",
    </3/0/12>;title="Init Bootstrapping";rt="Init Bootstrapping",
    </3/0/0>;title="Manufacturer";rt="Manufacturer",
    </3/0/1>;title="Model Number";rt="Model Number",
    </3/0/2>;title="Serial Number";rt="Serial Number",
    </3/0/3>;title="FW version";rt="FW version",
    </3/0/4>;title="Reboot";rt="Reboot",
    </3/0/5>;title="Factory Reset";rt="Factory Reset",
    </3/0/16>;title="HW version";rt="HW version",
    </4/0/4>;title="Ip";rt="IPv6",
    </3/0/14>;title="Tx powerl";rt="TX power",
    </3/0/15>;title="Channel: PUT value";rt="Channel",
    </10241/0/0>;title="TEM-HUM-BAT";obs,
    </10243/0/6>;title="factory_programming: PUT value";rt="factory_programming",
    </10243/0/10>;title="Router ip";rt="IPv6 Router",
    </10243/0/12>;title="ServerIp";rt="ServerIp",
    </10243/0/13>;title="Neighbours";rt="Neighbours",
    </10243/0/20>;title="HW version";rt="HW version",
    </10243/0/21>;title="HW version";rt="HW version",
    </5/0/0>;title="FW package can be updated using PUT method";rt="block";sz="MAX_PLUGFEST_BODY",
    </5/0/2>;title="fw_update";rt="fw_update",
    </5/0/3>;title="fw_state";rt="fw_state",
    </5/0/5>;title="fw_update_result";rt="fw_update_result",
    </3/0/10>


    coap get coap://192.168.3.164:15395/.well-known/core
    </.well-known/core>;ct=40,
    <//>;title="Default root resource",
    </0/1>;title="Security: PUT value";rt="Security",
    </1/1>;title="Server: PUT value";rt="Server",
    </3/0/12>;title="Init Bootstrapping";rt="Init Bootstrapping",
    </3/0/0>;title="Manufacturer";rt="Manufacturer",
    </3/0/1>;title="Model Number";rt="Model Number",
    </3/0/2>;title="Serial Number";rt="Serial Number",
    </3/0/3>;title="FW version";rt="FW version",
    </3/0/4>;title="Reboot";rt="Reboot",
    </3/0/5>;title="Factory Reset";rt="Factory Reset",
    </3/0/9>;title="Battery status";rt="Battery",
    </3/0/14>;title="Tx powerl";rt="TX power",
    </3/0/15>;title="Channel: PUT value";rt="Channel",
    </3/0/16>;title="HW version";rt="HW version",
    </5/0/0>;title="FW package can be updated using PUT method";rt="block";sz="MAX_PLUGFEST_BODY",
    </5/0/2>;title="fw_update";rt="fw_update",
    </5/0/3>;title="fw_state";rt="fw_state",
    </3/0/10>,
    </5/0/5>;title="fw_update_result";rt="fw_update_result",
    </10241/0/0>;title="TEM-HUM-BAT";obs,
    </10242/0/0>;title="Events";obs,
    </10243/0/1>;title="Cal Temp: PUT value";rt="Cal Temp",
    </10243/0/2>;title="Cal Hum: PUT value";rt="Cal Hum",
    </10243/0/6>;title="Hysteresis: PUT value";rt="Hysteresis",
    </10243/0/10>;title="Router ip";rt="IPv6 Router",
    </10243/0/11>;title="Error code";rt="HW",
    </10243/0/12>;title="ServerIp";rt="ServerIp",
    </10243/0/13>;title="Neighbours";rt="Neighbours",
    </10243/0/16>;title="SetPoint event";obs,
    </10244/0/0>;title="IR capture command,
    </10244/0/1>;title="IR Status Command";obs,
    </10244/0/2>;title="IR Send Command,
    </10244/0/3>;title="IR Autocheck: PUT value";rt="IR Autocheck",
    </10244/0/4>;title="IR TX Mode: PUT value";rt="IR TX Mode",
    </10243/0/20>;title="HW version";rt="HW version",
    </10243/0/21>;title="HW version";rt="HW version"


**Turning on**

.. code-block::

    PUT /10242/0/0
    Content-Format: 1541
    cm=cool,t=1335,sp=210

**Turning off**

.. code-block::

    PUT /10242/0/0
    Content-Format: 1541
    cm=cool,t=0,sp=off

References
----------

* https://www.momit.com/en-us/products/cool
* https://tools.ietf.org/html/draft-bormann-core-simple-server-discovery-01
* https://github.com/smikims/arpspoof
* http://coap.technology/
