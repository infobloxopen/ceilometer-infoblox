===============================
ceilometer-infoblox
===============================

Infoblox Custom Meters for Ceilometer

This package provides files used by OpenStack Ceilometer to monitor various DNS
and DHCP metrics from Infoblox NIOS instances. With this package installed
and configured, the Ceilometer Compute Agent will poll local NIOS instances
via SNMP, and store the results as samples with metric names starting with
'nios.dns' and 'nios.dhcp'.

* Free software: Apache license

Features
--------

This module enables SNMP polling of NIOS instances to collect DNS and DHCP
metrics.

OpenStack Configuration
-----------------------

After installing the package, you must configure Ceilometer with the SNMP
credentials, as well as tell it how to reach the NIOS machines.

Since the Ceilometer agent is running within the address space of the host
node, the grid member IP address used must be reachable from the host. This
can be done by allocating the IP on an external network, or by using a floating
IP.

By default, the first floating IP for a given instance will be used for SNMP
access. To override this behavior, you can set a ``infoblox-snmp-ip`` metadata
value on the instance.

Similarly, you may set the default SNMP community, password, and port in a
``[infoblox]`` stanza within the ``ceilometer.conf`` file, or you can set them
on a per-instance basis using instance metadata.

The table below summarizes the different options.

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Config File Variable
     - Instance Metadata Name
     - Description
   * - metadata_name
     - N/A
     - The name of the instance metadata item used to identify an instance as
       an Infoblox DDI appliance. Default value is ``infoblox``.
   * - N/A
     - infoblox-snmp-ip
     - By default the first floating IP found is used; set this value on the
       instance to specify a particular IP to be used for SNMP access.
   * - snmp_community_or_username
     - infoblox-snmp-community
     - The SNMP community for v2c, or the user name for SNMPv3. The default
       value is ``public``.
   * - snmp_password
     - infoblox-snmp-password
     - The SNMP password for SNMPv3.
   * - snmp_port
     - infoblox-snmp-port
     - The port to use for SNMP polling. Default value is ``161``.

You must also configure the security groups to allow UDP traffic to port 161
on the NIOS instances, from the host IP network.

Infoblox NIOS Configuration
---------------------------

You must enable SNMP for the grid or for the specific members which you would
like to poll. This is done in the Grid > Grid Manager screen, using the Grid
Properties button on the right-hand toolbar. This brings up an editor from
which you can select SNMP, enable it, and enter a community string.

Currently only SNMPv2c is tested.

