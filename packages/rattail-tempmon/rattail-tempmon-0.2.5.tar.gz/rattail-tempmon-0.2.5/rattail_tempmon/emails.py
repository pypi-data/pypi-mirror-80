# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Email config for tempmon-server
"""

from __future__ import unicode_literals, absolute_import

from rattail.db import model
from rattail.mail import Email
from rattail.time import localtime

from rattail_tempmon.db import model as tempmon


class TempmonBase(object):
    """
    Generic base class for all tempmon-related emails; adds common sample data.
    """
    
    def sample_data(self, request):
        now = localtime(self.config)
        client = tempmon.Client(config_key='testclient', hostname='testclient')
        probe = tempmon.Probe(config_key='testprobe', description="Test Probe",
                              good_max_timeout=45)
        client.probes.append(probe)
        return {
            'client': client,
            'probe': probe,
            'probe_url': '#',
            'status': self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_ERROR],
            'reading': tempmon.Reading(),
            'taken': now,
            'now': now,
            'status_since': now.strftime('%I:%M %p'),
            'status_since_delta': 'now',
            'recent_minutes': 90,
            'recent_readings': [],
        }


class tempmon_critical_high_temp(TempmonBase, Email):
    """
    Sent when a tempmon probe takes a "critical high" temperature reading.
    """
    default_subject = "CRITICAL HIGH Temperature"

    def sample_data(self, request):
        data = super(tempmon_critical_high_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_CRITICAL_HIGH_TEMP]
        return data


class tempmon_critical_low_temp(TempmonBase, Email):
    """
    Sent when a tempmon probe takes a "critical low" temperature reading.
    """
    default_subject = "CRITICAL LOW Temperature"

    def sample_data(self, request):
        data = super(tempmon_critical_low_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_CRITICAL_LOW_TEMP]
        return data


class tempmon_error(TempmonBase, Email):
    """
    Sent when a tempmon probe is noticed to have some error, i.e. no current readings.
    """
    default_subject = "Probe error detected"
    
    def sample_data(self, request):
        data = super(tempmon_error, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_ERROR]
        data['taken'] = None
        return data


class tempmon_client_offline(TempmonBase, Email):
    """
    Sent when a tempmon client has been marked offline.
    """
    default_subject = "Client Offline"


class tempmon_good_temp(TempmonBase, Email):
    """
    Sent whenever a tempmon probe first takes a "good temp" reading, after
    having previously had some bad reading(s).
    """
    default_subject = "OK Temperature"
    
    def sample_data(self, request):
        data = super(tempmon_good_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_GOOD_TEMP]
        return data


class tempmon_high_temp(TempmonBase, Email):
    """
    Sent when a tempmon probe takes a reading which is above the "maximum good
    temp" range, but still below the "critically high temp" threshold.
    """
    default_subject = "HIGH Temperature"
    
    def sample_data(self, request):
        data = super(tempmon_high_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_HIGH_TEMP]
        return data


class tempmon_low_temp(TempmonBase, Email):
    """
    Sent when a tempmon probe takes a reading which is below the "minimum good
    temp" range, but still above the "critically low temp" threshold.
    """
    default_subject = "LOW Temperature"

    def sample_data(self, request):
        data = super(tempmon_low_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_LOW_TEMP]
        return data


class tempmon_disabled_probes(Email):
    """
    Notifies of any Tempmon client devices or probes which are disabled.
    """
    default_subject = "Disabled probes"

    def sample_data(self, request):
        return {
            'disabled_clients': [
                tempmon.Client(config_key='foo', hostname='foo.example.com'),
            ],
            'disabled_probes': [
                tempmon.Probe(description="north wall of walk-in cooler",
                              client=tempmon.Client(config_key='bar')),
            ],
        }
