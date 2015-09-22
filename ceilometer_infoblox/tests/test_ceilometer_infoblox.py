# Copyright 2015 Infoblox, Inc.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_ceilometer_infoblox
----------------------------------

Tests for `ceilometer_infoblox` module.
"""
import mock

from oslo_config import cfg

from ceilometer.compute import discovery as compute_disc
from ceilometer_infoblox import discovery
from ceilometer_infoblox.tests import base


class TestCeilometer_infoblox(base.TestCase):

    def setUp(self):
        super(TestCeilometer_infoblox, self).setUp()
        cfg.CONF.set_override(name='management_network',
                              group='infoblox',
                              override='service-net')

    def _nios_server(self, nios):
        s = mock.MagicMock()
        if nios:
            p = mock.PropertyMock(return_value={'nios': 'true'})
        else:
            p = mock.PropertyMock(return_value={})

        type(s).metadata = p

        addr_list = {
            'mgmt-net': [
                {
                    'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:7d:74:28',
                    'version': 4, 'addr': '10.1.0.3',
                    'OS-EXT-IPS:type': 'fixed'
                }
            ],
            'service-net': [
                {
                    'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:e5:ab:87',
                    'version': 4, 'addr': '10.2.0.3',
                    'OS-EXT-IPS:type': 'fixed'
                },
                {
                    'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:e5:ab:87',
                    'version': 4, 'addr': '172.16.98.67',
                    'OS-EXT-IPS:type': 'floating'
                }
            ]
        }

        type(s).addresses = mock.PropertyMock(return_value=addr_list)

        return s

    def test_discovery_nios(self):
        server_list = [self._nios_server(True), self._nios_server(False)]
        d = mock.MagicMock()
        d.return_value = server_list
        compute_disc.InstanceDiscovery.discover = d
        nios_disc = discovery.NIOSDiscovery()
        self.assertEqual(len(nios_disc.discover(mock.MagicMock())), 1)

    def test_discovery_nios_no_port(self):
        server_list = [self._nios_server(True), self._nios_server(False)]
        d = mock.MagicMock()
        d.return_value = server_list
        compute_disc.InstanceDiscovery.discover = d
        cfg.CONF.set_override(name='management_network',
                              group='infoblox',
                              override='junk')
        nios_disc = discovery.NIOSDiscovery()
        self.assertEqual(len(nios_disc.discover(mock.MagicMock())), 0)

    def test_discovery_nios_no_fip(self):
        server_list = [self._nios_server(True), self._nios_server(False)]
        d = mock.MagicMock()
        d.return_value = server_list
        compute_disc.InstanceDiscovery.discover = d
        cfg.CONF.set_override(name='management_network',
                              group='infoblox',
                              override='mgmt-net')
        nios_disc = discovery.NIOSDiscovery()
        self.assertEqual(len(nios_disc.discover(mock.MagicMock())), 0)

    def test_discovery_nios_no_use_fip(self):
        server_list = [self._nios_server(True), self._nios_server(False)]
        d = mock.MagicMock()
        d.return_value = server_list
        compute_disc.InstanceDiscovery.discover = d
        cfg.CONF.set_override(name='use_floating_ip',
                              group='infoblox',
                              override=False)
        nios_disc = discovery.NIOSDiscovery()
        self.assertEqual(len(nios_disc.discover(mock.MagicMock())), 1)
