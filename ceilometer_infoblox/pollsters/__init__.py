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

from ceilometer.hardware.pollsters import generic
from ceilometer import sample


@six.add_metaclass(abc.ABCMeta)
class BaseNIOSPollster(generic.GenericHardwareDeclarativePollster):

    def __init__(self):
        super(BaseNIOSPollster, self).__init__()

        meter = generic.MeterDefinition(self.meter_dict)
        self._update_meter_definition(meter)

    @property
    def default_discovery(self):
        return 'nios_instances'

    def generate_samples(self, host_url, data):
        """Generate a list of Sample from the data returned by inspector

        :param host_url: host url of the endpoint
        :param data: list of data returned by the corresponding inspector
        """
        samples = []
        definition = self.meter_definition
        for (value, metadata, extra) in data:
            s = sample.Sample(
                name=definition.name,
                type=definition.type,
                unit=definition.unit,
                volume=value,
                user_id=extra['user_id'],
                project_id=extra['tenant_id'],
                resource_id=extra['resource_id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=extra,
            )
            samples.append(s)
        return samples
