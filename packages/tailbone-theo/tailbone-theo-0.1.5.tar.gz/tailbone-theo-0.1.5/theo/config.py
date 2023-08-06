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
Configuration for Theo
"""

from rattail.config import ConfigExtension


class TheoConfig(ConfigExtension):
    """
    Rattail config extension for Theo
    """
    key = 'theo'

    def configure(self, config):

        # call the app "Theo" by default
        config.setdefault('rattail', 'app_title', "Theo")

        # Theo comes with its own menu for web app
        config.setdefault('tailbone', 'menus', 'theo.web.menus')

        # custom App Settings
        config.setdefault('rattail', 'settings', 'theo.appsettings')

        # do we integrate w/ CORE-POS?
        if integrate_corepos(config):
            config.setdefault('rattail', 'model', 'theo.db.model_corepos')
            config.setdefault('rattail.mail', 'emails', 'theo.emails.theo, theo.emails.corepos')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_corepos:FromTheoToTheoVersions')

        # do we integrate w/ Catapult?
        elif integrate_catapult(config):
            config.setdefault('rattail', 'model', 'theo.db.model_catapult')
            config.setdefault('rattail.mail', 'emails', 'theo.emails.theo, theo.emails.catapult')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_catapult:FromTheoToTheoVersions')

        # do we integrate w/ LOC SMS?
        elif integrate_locsms(config):
            config.setdefault('rattail', 'model', 'theo.db.model_locsms')
            config.setdefault('rattail.mail', 'emails', 'theo.emails.theo, theo.emails.locsms')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_locsms:FromTheoToTheoVersions')

        else: # no integration
            config.setdefault('rattail.mail', 'emails', 'theo.emails.theo')


def integrate_catapult(config):
    return config.getbool('theo', 'integrate_catapult', default=False,
                          usedb=False)


def integrate_corepos(config):
    return config.getbool('theo', 'integrate_corepos', default=False,
                          usedb=False)


def integrate_locsms(config):
    return config.getbool('theo', 'integrate_locsms', default=False,
                          usedb=False)
