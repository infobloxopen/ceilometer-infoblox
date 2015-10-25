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

import abc

from oslo_utils import timeutils
import six

from ceilometer.hardware import plugin
from ceilometer import sample

from ceilometer_infoblox import inspector as ins


@six.add_metaclass(abc.ABCMeta)
class BaseNIOSPollster(plugin.HardwarePollster):

    def __init__(self):
        super(BaseNIOSPollster, self).__init__()

    @property
    def default_discovery(self):
        return 'nios_instances'

    def generate_one_sample(self, host_url, datum):
        value, metadata, extra = datum
        return sample.Sample(
            name=self.meter_name,
            type=self.meter_type,
            unit=self.meter_unit,
            volume=value,
            user_id=extra['user_id'],
            project_id=extra['tenant_id'],
            resource_id=extra['resource_id'],
            timestamp=timeutils.utcnow().isoformat(),
            resource_metadata=extra,
        )

    def _get_inspector(self, parsed_url):
        if parsed_url.scheme not in self.inspectors:
            driver = ins.NIOSInspector()
            self.inspectors[parsed_url.scheme] = driver
        return self.inspectors[parsed_url.scheme]
