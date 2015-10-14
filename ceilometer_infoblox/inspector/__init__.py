#
# Copyright 2015 Infoblox, Inc.
#
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
"""Inspector for collecting Infoblox-specific data over SNMP"""

from ceilometer.hardware.inspector import snmp


class NIOSInspector(snmp.SNMPInspector):

    OID_DNS_STATS = '1.3.6.1.4.1.7779.3.1.1.3.1'
    OID_DHCP_STATS = '1.3.6.1.4.1.7779.3.1.1.4.1.3'

    def _make_mapping(name, base_oid, oid):
        return ('nios.%s' % name, {
            'matching_type': snmp.EXACT,
            'metric_oid': (base_oid + oid, int),
            'metadata': {},
            'post_op': None
        })

    MAPPING = dict([
        _make_mapping('dns.qps', OID_DNS_STATS, '.6.0'),
        _make_mapping('dns.chr', OID_DNS_STATS, '.5.0'),
        _make_mapping('dhcp.discovers', OID_DHCP_STATS, '.1.0'),
        _make_mapping('dhcp.requests', OID_DHCP_STATS, '.2.0'),
        _make_mapping('dhcp.releases', OID_DHCP_STATS, '.3.0'),
        _make_mapping('dhcp.offers', OID_DHCP_STATS, '.4.0'),
        _make_mapping('dhcp.acks', OID_DHCP_STATS, '.5.0'),
        _make_mapping('dhcp.nacks', OID_DHCP_STATS, '.6.0'),
        _make_mapping('dhcp.declines', OID_DHCP_STATS, '.7.0'),
        _make_mapping('dhcp.informs', OID_DHCP_STATS, '.8.0'),
        _make_mapping('dhcp.others', OID_DHCP_STATS, '.9.0')])

    def __init__(self):
        super(NIOSInspector, self).__init__()
