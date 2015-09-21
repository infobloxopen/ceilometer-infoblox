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

from oslo_log import log as logger
from oslo_utils import netutils
import six

from ceilometer.compute import pollsters
from ceilometer.compute.pollsters import util
from ceilometer.hardware.inspector import snmp
from ceilometer.i18n import _
from ceilometer import sample

from ceilometer_infoblox import config as cfg
from ceilometer_infoblox.inspectors import snmp as nios

LOG = logger.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class BaseNIOSPollster(pollsters.BaseComputePollster):

    OID_SYSUPTIME = '1.3.6.1.2.1.1.3.0'

    OID_IB_ONE = '1.3.6.1.4.1.7779.3.1.1'
    OID_IB_PLATFORM_ONE = OID_IB_ONE + '.2'
    OID_IB_DNS_ONE = OID_IB_ONE + '.3'
    OID_IB_DHCP_ONE = OID_IB_ONE + '.4'

    OID_IB_DNS_XFR = OID_IB_DNS_ONE + '.1.4.0'
    OID_IB_DNS_CHR = OID_IB_DNS_ONE + '.1.5.0'
    OID_IB_DNS_QPS = OID_IB_DNS_ONE + '.1.6.0'

    OID_IB_DHCP_STATS = OID_IB_DHCP_ONE + '.1.3'

    OID_IB_DHCP_DISCOVERS = OID_IB_DHCP_STATS + '.1'
    OID_IB_DHCP_REQUESTS = OID_IB_DHCP_STATS + '.2'
    OID_IB_DHCP_RELEASES = OID_IB_DHCP_STATS + '.3'
    OID_IB_DHCP_OFFERS = OID_IB_DHCP_STATS + '.4'
    OID_IB_DHCP_ACKS = OID_IB_DHCP_STATS + '.5'
    OID_IB_DHCP_NACKS = OID_IB_DHCP_STATS + '.6'
    OID_IB_DHCP_DECLINES = OID_IB_DHCP_STATS + '.7'
    OID_IB_DHCP_INFORMS = OID_IB_DHCP_STATS + '.8'
    OID_IB_DHCP_OTHERS = OID_IB_DHCP_STATS + '.9'

    def metric_oid(self):
        return self.OID_SYSUPTIME

    def metric_converter(self):
        return int

    def metric_name(self):
        return 'uptime'

    def metric_type(self):
        return sample.TYPE_CUMULATIVE

    def metric_unit(self):
        return 'seconds'

    def matching_type(self):
        return snmp.EXACT

    def inspector_param(self):
        return {
            'matching_type': self.matching_type(),
            'metric_oid': (self.metric_oid(), self.metric_converter()),
            'post_op': None,
            'metadata': {}
        }

    def extra_metadata(self):
        return None

    @property
    def inspector(self):
        inspector = getattr(self, '_inspector', None)
        if not isinstance(inspector, nios.SNMPInspector):
            inspector = nios.SNMPInspector()
            BaseNIOSPollster._inspector = inspector
        return inspector

    def _instance_ip(self, instance):
        mgmt_network = cfg.CONF['infoblox'].management_network
        use_floating = cfg.CONF['infoblox'].use_floating_ip

        port = instance.addresses.get(mgmt_network, None)
        if port is None:
            raise ValueError(_('Instance %(id)s does not have a port on '
                             'network %(net)s') % ({'id': instance.id,
                                                    'net': mgmt_network}))

        # Only IPv4 for now
        use_ip = None
        for ip in port:
            if ip['version'] != 4:
                continue
            if use_floating and ip['OS-EXT-IPS:type'] != 'floating':
                continue
            use_ip = ip['addr']
            break

        return use_ip

    def get_samples(self, manager, cache, resources):
        self._inspection_duration = self._record_poll_time()
        username = cfg.CONF['infoblox'].snmp_community_or_username
        password = cfg.CONF['infoblox'].snmp_password
        port = cfg.CONF['infoblox'].snmp_port
        for instance in resources:
            try:
                ip_addr = self._instance_ip(instance)
                if password:
                    url = ('snmp://%s:%s@%s:%d' %
                           (username, password, ip_addr, port))
                else:
                    url = 'snmp://%s@%s:%d' % (username, ip_addr, port)
                i_cache = {}
                LOG.debug('Checking %s for instance %s using IP %s',
                          self.metric_name(), instance, ip_addr)
                result = list(self.inspector.inspect_generic(
                    host=netutils.urlsplit(url),
                    cache=i_cache,
                    extra_metadata=self.extra_metadata(),
                    param=self.inspector_param()))
                LOG.debug("SNMP: %(instance)s result %(result)s",
                          {'instance': instance,
                           'result': result})
                yield util.make_sample_from_instance(
                    instance,
                    name=self.metric_name(),
                    type=self.metric_type(),
                    unit=self.metric_unit(),
                    volume=result[0][0]
                )
            except Exception as err:
                LOG.exception(_('Could not get %(name)s for %(id)s: %(e)s'),
                              {'name': self.metric_name(),
                               'id': instance.id, 'e': err})
