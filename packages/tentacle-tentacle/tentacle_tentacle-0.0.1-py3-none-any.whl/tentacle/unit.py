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


class Unit:
    def __init__(self, name, value, unit, range=[]):
        self.name = name
        self.value = value
        self.unit = unit


class Temperature(Unit):
    def __init__(self, value, unit='°C'):
        super().__init__('temperature', value, unit)


class Pressure(Unit):
    def __init__(self, value, unit='hPa'):
        super().__init__('pressure', value, unit)


class Relative_Humidity(Unit):
    def __init__(self, value, unit='%RH'):
        super().__init__('relative_humidity', value, unit)
