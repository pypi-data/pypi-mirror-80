# coding: utf-8

# Copyright (C) 2020 willipink.eu
# Author Moritz Münch moritzmuench@mailbox.org
# Author Thorben Willert thorben.w@posteo.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from calendar import timegm
from datetime import datetime


class Measurements:
    ''' measurements object to hold one or more capabilitites and a timestamp '''

    def __init__(self, *capabilities):
        self.timestamp = timegm(datetime.utcnow().utctimetuple())
        if capabilities:
            for capability in capabilities:
                setattr(self, capability.name, capability)


class Capability:

    def __init__(self, unit, range)
        self.unit = unit
        self.range = range
