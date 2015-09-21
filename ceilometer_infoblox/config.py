# Copyright 2015 Infoblox Inc.
# All Rights Reserved.
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

CONF = cfg.CONF

CONF.register_group(cfg.OptGroup(
    name='infoblox', title="Configuration for Infoblox Meters"
))

OPTS = [
    cfg.StrOpt('snmp_community_or_username'),
    cfg.StrOpt('snmp_password'),
    cfg.IntOpt('snmp_port', default=161),
    cfg.StrOpt('management_network'),
    cfg.BoolOpt('use_floating_ip', default=True),
]

CONF.register_opts(OPTS, group='infoblox')
