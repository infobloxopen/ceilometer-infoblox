# -*- encoding: utf-8 -*-
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

from oslo_config import cfg

from ceilometer.compute import discovery
from ceilometer.openstack.common import log

LOG = log.getLogger(__name__)

cfg.CONF.register_group(cfg.OptGroup(
    name='infoblox', title="Configuration for Infoblox Meters"
))

OPTS = [
    cfg.StrOpt('snmp_community_or_username'),
    cfg.StrOpt('snmp_password'),
    cfg.IntOpt('snmp_port', default=161),
    cfg.StrOpt('management_network'),
    cfg.BoolOpt('use_floating_ip', default=True),
    cfg.StrOpt('metadata_name', default='nios')
]

cfg.CONF.register_opts(OPTS, group='infoblox')


class NIOSDiscovery(discovery.InstanceDiscovery):
    def __init__(self):
        super(NIOSDiscovery, self).__init__()

    @property
    def management_network(self):
        return cfg.CONF['infoblox'].management_network

    @property
    def use_floating(self):
        return cfg.CONF['infoblox'].use_floating_ip

    def _instance_ip(self, instance):
        port = instance.addresses[self.management_network]

        # Only IPv4 for now
        use_ip = None
        for ip in port:
            if ip['version'] != 4:
                continue
            if self.use_floating and ip['OS-EXT-IPS:type'] != 'floating':
                continue
            use_ip = ip['addr']
            break

        # Treat no IP found the same as invalid network name
        if use_ip is None:
            raise KeyError

        return use_ip

    def discover(self, manager, param=None):
        instances = super(NIOSDiscovery, self).discover(manager, param)
        username = cfg.CONF['infoblox'].snmp_community_or_username
        password = cfg.CONF['infoblox'].snmp_password
        port = cfg.CONF['infoblox'].snmp_port
        metadata_name = cfg.CONF['infoblox'].metadata_name

        resources = []
        for instance in instances:
            try:
                metadata_value = instance.metadata.get(metadata_name, None)
                if metadata_value is None:
                    LOG.debug("Skipping instance %s; not tagged with '%s' "
                              "metadata tag." % (instance.id, metadata_name))
                    continue

                # Copy the Nova metering.stack meta-data to this resource,
                # so that standard autoscale code will work without custom
                # filtering.
                metering_stack = instance.metadata.get("metering.stack", None)

                ip_addr = self._instance_ip(instance)
                if password:
                    url = ('snmp://%s:%s@%s:%d' %
                           (username, password, ip_addr, port))
                else:
                    url = 'snmp://%s@%s:%d' % (username, ip_addr, port)

                i_type = instance.flavor['name'] if instance.flavor else None
                resource = {
                    'display_name': instance.name,
                    'name': getattr(instance,
                                    'OS-EXT-SRV-ATTR:instance_name', u''),
                    'instance_type': i_type,
                    metadata_name: metadata_value,
                    'host': instance.hostId,
                    'flavor': instance.flavor,
                    'status': instance.status.lower(),
                    'resource_id': instance.id,
                    'resource_url': url,
                    'user_id': instance.user_id,
                    'tenant_id': instance.tenant_id,
                    'metering.stack': metering_stack
                }

                resources.append(resource)
            except KeyError:
                LOG.error(
                    ("Couldn't obtain %(type)s IP address for network "
                     " %(network)s of instance %(id)s")
                    % ({'type': 'floating' if self.use_floating else 'fixed',
                        'network': self.management_network,
                        'id': instance.id})
                )

        return resources
