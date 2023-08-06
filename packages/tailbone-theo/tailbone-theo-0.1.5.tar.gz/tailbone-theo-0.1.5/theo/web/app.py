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
Theo web app
"""

from tailbone import app

from theo.config import integrate_catapult, integrate_corepos, integrate_locsms


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # establish rattail config
    rattail_config = app.make_rattail_config(settings)

    # which template directories we want depends on integration
    directories = ['theo.web:templates']
    if integrate_corepos(rattail_config):
        directories.append('tailbone_corepos:templates')
    if integrate_catapult(rattail_config):
        directories.append('tailbone_onager:templates')
    if integrate_locsms(rattail_config):
        directories.append('tailbone_locsms:templates')
    directories.append('tailbone:templates')
    settings.setdefault('mako.directories', directories)

    # for graceful handling of postgres restart
    settings.setdefault('retry.attempts', 2)

    # establish pyramid config
    pyramid_config = app.make_pyramid_config(settings)

    # maybe configure integration db connections
    if integrate_catapult(rattail_config):
        from tailbone_onager.db import CatapultSession
        CatapultSession.configure(bind=rattail_config.catapult_engine)
    if integrate_corepos(rattail_config):
        from tailbone_corepos.db import CoreOfficeSession
        CoreOfficeSession.configure(bind=rattail_config.corepos_engine)
    if integrate_locsms(rattail_config):
        from tailbone_locsms.db import SmsSession
        SmsSession.configure(bind=rattail_config.locsms_engine)

    # bring in the rest of Theo
    pyramid_config.include('theo.web.static')
    pyramid_config.include('theo.web.subscribers')
    pyramid_config.include('theo.web.views')

    # for graceful handling of postgres restart
    pyramid_config.add_tween('tailbone.tweens.sqlerror_tween_factory',
                             under='pyramid_tm.tm_tween_factory')

    return pyramid_config.make_wsgi_app()
