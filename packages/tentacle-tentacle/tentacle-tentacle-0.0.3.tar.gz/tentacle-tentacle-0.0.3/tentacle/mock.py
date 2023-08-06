# coding: utf-8

# Copyright (C) 2018-20 willipink.eu
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


def mock_oserror(*args, **kwargs):
    ''' mock helper to raise an OSError '''
    raise OSError


def mock_filenotfounderror(*args, **kwargs):
    ''' mock helper to raise a FileNotFoundError '''
    raise FileNotFoundError


def mock_none(*args, **kwargs):
    ''' mock helper to return none '''
    return None
