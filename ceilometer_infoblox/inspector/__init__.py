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

    MAPPING = {
        'nios.dns.qps': {
            'matching_type': 'exact',
            'metric_oid': ('1.3.6.1.4.1.7779.3.1.1.3.1.6.0', int),
            'metadata': {},
            'post_op': None
        },
    }

    def __init__(self):
        super(NIOSInspector, self).__init__()
