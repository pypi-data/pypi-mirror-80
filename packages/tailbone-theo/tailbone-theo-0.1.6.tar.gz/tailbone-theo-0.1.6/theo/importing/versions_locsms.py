# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2020 Lance Edgar
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
Theo -> Theo "versions" data import, w/ LOC SMS integration
"""

from rattail.importing import versions as base
from rattail_luckysmores.importing.versions import LocVersionMixin


class FromTheoToTheoVersions(base.FromRattailToRattailVersions,
                             LocVersionMixin):
    """
    Handler for Theo -> Theo "versions" data import
    """

    def get_importers(self):
        importers = super(FromTheoToTheoVersions, self).get_importers()
        importers = self.add_locsms_importers(importers)
        return importers
