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
Common views
"""

from tailbone.views import common as base

import theo
from theo.config import integrate_catapult, integrate_corepos


class CommonView(base.CommonView):

    project_title = "tailbone-theo"
    project_version = theo.__version__

    def get_packages(self):
        packages = super(CommonView, self).get_packages()

        if integrate_catapult(self.rattail_config):
            import onager
            import rattail_onager
            import tailbone_onager
            packages['onager'] = onager.__version__
            packages['rattail-onager'] = rattail_onager.__version__
            packages['tailbone-onager'] = tailbone_onager.__version__

        elif integrate_corepos(self.rattail_config):
            import corepos
            import rattail_corepos
            import tailbone_corepos
            packages['pyCOREPOS'] = corepos.__version__
            packages['rattail-corepos'] = rattail_corepos.__version__
            packages['tailbone-corepos'] = tailbone_corepos.__version__

        return packages


def includeme(config):
    CommonView.defaults(config)
