===============================
ceilometer-infoblox
===============================

Infoblox Custom Meters for Ceilometer

This package provides files used by OpenStack Ceilometer to monitor the DNS
queries-per-second from Infoblox NIOS instances. With this package installed
and configured, the Ceilometer Compute Agent will poll local NIOS instances
via SNMP, and store the results as samples with the metric name 'nios.dns.qps'.

* Free software: Apache license

Features
--------

This module enables SNMP polling of NIOS instances to collect DNS queries per
second.

OpenStack Configuration
-----------------------

After installing the package, you must configure Ceilometer with the SNMP
credentials, as well as tell it how to reach the NIOS machines.

Since the Ceilometer agent is running within the address space of the host
node, the grid member IP address used must be reachable from the host. This
can be done by allocating the IP on an external network, or by using a floating
IP.

To configure the Ceilometer agent, you must set the following parameters in a
``[infoblox]`` stanza within the ``ceilometer.conf`` file.

*management_network* - this is the name of the OpenStack network for the port
that should be used to poll the NIOS instance. If you have only set up LAN1,
then this should be the network to which LAN1 is attached.

*use_floating_ip* - if subnets on the ``management_network`` are not directly
reachable from the host, then you must use a floating IP address and set this
to ``True``. This will cause the polling agent to use the floating IP address
associated with the fixed IP address that is on the port attached to the 
``management_network``. Default value is ``True``.

*metadata_name* - only instances with a port on the ``management_network`` and
flagged with the metadata named here will be polled. Note that the *value* of
the metadata does not matter; if the key exists, that instance will be polled.
Default value is ``nios``.

*snmp_community_or_username* - the SNMP community for v2c, or the user name for
SNMPv3.

*snmp_password* - the SNMP password for SNMPv3.

*snmp_port* - the port to use for SNMP polling. Default value is ``161``.


*Example Ceilometer Configuration*

::

 [infoblox]
 management_network = service-net
 use_floating_ip = True
 snmp_community_or_username = public

You must also configure the security groups to allow UDP traffic to port 161
on the NIOS instances, from the host IP network.

Infoblox NIOS Configuration
---------------------------

You must enable SNMP for the grid or for the specific members which you would
like to poll. This is done in the Grid > Grid Manager screen, using the Grid
Properties button on the right-hand toolbar. This brings up an editor from
which you can select SNMP, enable it, and enter a community string.

Currently only SNMPv2c is tested.

