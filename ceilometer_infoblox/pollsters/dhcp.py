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

from ceilometer_infoblox import pollsters


class DHCPPollster(pollsters.BaseNIOSPollster):

    def __init__(self):
        super(DHCPPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.invalid'
    BASE_OID = '1.3.6.1.4.1.7779.3.1.1.4.1.3'

    @property
    def meter_type(self):
        return 'cumulative'

    @property
    def meter_unit(self):
        return 'messages'


class DiscoversPollster(DHCPPollster):

    def __init__(self):
        super(DiscoversPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.discovers'
    OID = '.1.0'


class RequestsPollster(DHCPPollster):

    def __init__(self):
        super(RequestsPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.requests'
    OID = '.2.0'


class ReleasesPollster(DHCPPollster):

    def __init__(self):
        super(ReleasesPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.releases'
    OID = '.3.0'


class OffersPollster(DHCPPollster):

    def __init__(self):
        super(OffersPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.offers'
    OID = '.4.0'


class AcksPollster(DHCPPollster):

    def __init__(self):
        super(AcksPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.acks'
    OID = '.5.0'


class NacksPollster(DHCPPollster):

    def __init__(self):
        super(NacksPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.nacks'
    OID = '.6.0'


class DeclinesPollster(DHCPPollster):

    def __init__(self):
        super(DeclinesPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.declines'
    OID = '.7.0'


class InformsPollster(DHCPPollster):

    def __init__(self):
        super(InformsPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.informs'
    OID = '.8.0'


class OthersPollster(DHCPPollster):

    def __init__(self):
        super(OthersPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.others'
    OID = '.9.0'
