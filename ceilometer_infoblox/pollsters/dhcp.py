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

    @property
    def meter_name(self):
        return self.IDENTIFIER

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


class RequestsPollster(DHCPPollster):

    def __init__(self):
        super(RequestsPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.requests'


class ReleasesPollster(DHCPPollster):

    def __init__(self):
        super(ReleasesPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.releases'


class OffersPollster(DHCPPollster):

    def __init__(self):
        super(OffersPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.offers'


class AcksPollster(DHCPPollster):

    def __init__(self):
        super(AcksPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.acks'


class NacksPollster(DHCPPollster):

    def __init__(self):
        super(NacksPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.nacks'


class DeclinesPollster(DHCPPollster):

    def __init__(self):
        super(DeclinesPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.declines'


class InformsPollster(DHCPPollster):

    def __init__(self):
        super(InformsPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.informs'


class OthersPollster(DHCPPollster):

    def __init__(self):
        super(OthersPollster, self).__init__()

    IDENTIFIER = 'nios.dhcp.others'
