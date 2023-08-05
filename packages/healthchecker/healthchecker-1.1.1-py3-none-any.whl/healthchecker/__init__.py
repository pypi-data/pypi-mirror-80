"""HealthChecker: check sites health and publish results in a file in Github."""

# -----------------------------------------------------------------------------
# Copyright (C) 2019 HacKan (https://hackan.net)
#
# This file is part of HealthChecker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from .core import healthcheck_url
from .core import healthcheck_urls
from .core import notify
from .objects import ServiceStatus
from .objects import ServiceStatusList

__version__ = '1.1.0'
__license__ = 'GPL-3.0+'
__author__ = 'HacKan (https://hackan.net)'

__all__ = (
    'healthcheck_url',
    'healthcheck_urls',
    'notify',
    'ServiceStatus',
    'ServiceStatusList',
    '__version__',
)
