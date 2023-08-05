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
Theo -> Theo "versions" data import, w/ CORE-POS integration
"""

from rattail.importing import versions as base
from rattail_corepos.importing.versions import CoreposVersionMixin


class FromTheoToTheoVersions(base.FromRattailToRattailVersions,
                             CoreposVersionMixin):
    """
    Handler for Theo -> Theo "versions" data import
    """
    host_title = "Theo"
    local_title = "Theo (versioning)"

    def get_importers(self):
        importers = super(FromTheoToTheoVersions, self).get_importers()
        importers = self.add_corepos_importers(importers)
        return importers
