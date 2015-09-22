#
# Copyright 2012 eNovance <licensing@enovance.com>
# Copyright 2012 Red Hat, Inc
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

from ceilometer_infoblox import pollsters


class QPSPollster(pollsters.BaseNIOSPollster):

    def __init__(self):
        super(QPSPollster, self).__init__()

    @property
    def meter_dict(self):
        return {
            'name': 'nios.dns.qps',
            'unit': 'queries/s',
            'type': 'gauge',
            'snmp_inspector': {
                'matching_type': 'exact',
                'oid': '1.3.6.1.4.1.7779.3.1.1.3.1.6.0',
                'type': 'int'
            }
        }
