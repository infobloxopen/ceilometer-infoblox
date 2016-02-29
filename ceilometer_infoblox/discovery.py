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
from oslo_log import log

from ceilometer.compute import discovery
from ceilometer.i18n import _

LOG = log.getLogger(__name__)
MD_SNMP_IP = 'infoblox-snmp-ip'
MD_SNMP_PORT = 'infoblox-snmp-port'
MD_SNMP_USER = 'infoblox-snmp-community'
MD_SNMP_PASS = 'infoblox-snmp-password'
MD_IB_METADATA = 'infoblox'
CFG_GROUP = 'infoblox'

cfg.CONF.register_group(cfg.OptGroup(
    name=CFG_GROUP, title="Configuration for Infoblox Meters"
))

OPTS = [
    cfg.StrOpt('snmp_community_or_username', default='public'),
    cfg.StrOpt('snmp_password'),
    cfg.IntOpt('snmp_port', default=161),
    cfg.StrOpt('metadata_name', default=MD_IB_METADATA)
]

cfg.CONF.register_opts(OPTS, group=CFG_GROUP)


class NIOSDiscovery(discovery.InstanceDiscovery):
    def __init__(self):
        super(NIOSDiscovery, self).__init__()

    @property
    def management_network(self):
        return cfg.CONF[CFG_GROUP].management_network

    @property
    def md_name(self):
        return cfg.CONF[CFG_GROUP].metadata_name

    @property
    def default_snmp_port(self):
        return cfg.CONF[CFG_GROUP].snmp_port

    @property
    def default_snmp_username(self):
        return cfg.CONF[CFG_GROUP].snmp_community_or_username

    @property
    def default_snmp_password(self):
        return cfg.CONF[CFG_GROUP].snmp_password

    def _instance_url(self, instance):
        user = instance.metadata.get(MD_SNMP_USER, self.default_snmp_username)
        pw = instance.metadata.get(MD_SNMP_PASS, self.default_snmp_password)
        snmp_port = instance.metadata.get(MD_SNMP_PORT, self.default_snmp_port)

        ip = instance.metadata.get(MD_SNMP_IP, None)
        if ip is None:
            for port in instance.addresses.values():
                for port_ip in port:
                    # Only IPv4 for now
                    if port_ip['version'] != 4:
                        continue
                    if port_ip['OS-EXT-IPS:type'] != 'floating':
                        continue
                    ip = port_ip['addr']
                    break

        if ip is None:
            raise KeyError

        if pw:
            url = 'snmp://%s:%s@%s:%d' % (user, pw, ip, snmp_port)
        else:
            url = 'snmp://%s@%s:%d' % (user, ip, snmp_port)

        return url

    def discover(self, manager, param=None):
        instances = super(NIOSDiscovery, self).discover(manager, param)
        resources = []
        for instance in instances:
            try:
                md_value = instance.metadata.get(self.md_name, None)
                if md_value is None:
                    LOG.debug("Skipping instance %s; not tagged with '%s' "
                              "metadata tag." % (instance.id, self.md_name))
                    continue

                # Copy the Nova metering.stack meta-data to this resource,
                # so that standard autoscale code will work without custom
                # filtering.
                metering_stack = instance.metadata.get("metering.stack", None)

                url = self._instance_url(instance)
                i_type = instance.flavor['name'] if instance.flavor else None
                resource = {
                    'display_name': instance.name,
                    'name': getattr(instance,
                                    'OS-EXT-SRV-ATTR:instance_name', u''),
                    'instance_type': i_type,
                    self.md_name: md_value,
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
                    _("Could not determine SNMP IP address for instance %s.")
                    % instance.id
                )

        return resources
