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

from ceilometer import sample
from ceilometer_infoblox import pollsters


class QPSPollster(pollsters.BaseNIOSPollster):

    def metric_oid(self):
        return self.OID_IB_DNS_QPS

    def metric_converter(self):
        return int

    def metric_name(self):
        return 'nios.dns.qps'

    def metric_unit(self):
        return 'queries/s'

    def metric_type(self):
        return sample.TYPE_GAUGE
