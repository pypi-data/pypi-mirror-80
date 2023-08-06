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
Views
"""

from theo.config import integrate_catapult, integrate_corepos, integrate_locsms


def includeme(config):
    rattail_config = config.registry.settings.get('rattail_config')

    # core views
    config.include('theo.web.views.common')
    config.include('tailbone.views.auth')
    config.include('tailbone.views.tables')
    config.include('tailbone.views.upgrades')
    config.include('tailbone.views.progress')

    # main table views
    config.include('tailbone.views.customergroups')
    config.include('tailbone.views.custorders')
    config.include('tailbone.views.datasync')
    config.include('tailbone.views.email')
    config.include('tailbone.views.messages')
    config.include('tailbone.views.reportcodes')
    config.include('tailbone.views.roles')
    config.include('tailbone.views.settings')
    config.include('tailbone.views.users')

    # do we integrate w/ Catapult?
    if integrate_catapult(rattail_config):
        config.include('tailbone_onager.views.stores')
        config.include('tailbone_onager.views.customers')
        config.include('tailbone.views.members')
        config.include('tailbone_onager.views.employees')
        config.include('tailbone.views.people')
        config.include('tailbone_onager.views.taxes')
        config.include('tailbone_onager.views.departments')
        config.include('tailbone.views.subdepartments')
        config.include('tailbone_onager.views.brands')
        config.include('tailbone_onager.views.vendors')
        config.include('tailbone_onager.views.products')
        config.include('tailbone_onager.views.catapult')

    # do we integrate w/ CORE-POS?
    elif integrate_corepos(rattail_config):
        config.include('tailbone.views.stores')
        config.include('tailbone_corepos.views.customers')
        config.include('tailbone_corepos.views.members')
        config.include('tailbone.views.employees')
        config.include('tailbone_corepos.views.people')
        config.include('tailbone.views.taxes')
        config.include('tailbone_corepos.views.departments')
        config.include('tailbone_corepos.views.subdepartments')
        config.include('tailbone.views.brands')
        config.include('tailbone_corepos.views.vendors')
        config.include('tailbone_corepos.views.products')
        config.include('tailbone_corepos.views.corepos')

    # do we integrate w/ LOC SMS?
    elif integrate_locsms(rattail_config):
        config.include('tailbone.views.stores')
        config.include('tailbone.views.customers')
        config.include('tailbone.views.members')
        config.include('tailbone.views.employees')
        config.include('tailbone.views.people')
        config.include('tailbone.views.taxes')
        config.include('tailbone.views.departments')
        config.include('tailbone.views.subdepartments')
        config.include('tailbone.views.brands')
        config.include('tailbone.views.vendors')
        config.include('tailbone.views.products')
        config.include('tailbone_locsms.views.locsms')

    else: # no POS integration
        config.include('tailbone.views.stores')
        config.include('tailbone.views.customers')
        config.include('tailbone.views.members')
        config.include('tailbone.views.employees')
        config.include('tailbone.views.people')
        config.include('tailbone.views.taxes')
        config.include('tailbone.views.departments')
        config.include('tailbone.views.subdepartments')
        config.include('tailbone.views.brands')
        config.include('tailbone.views.vendors')
        config.include('tailbone.views.products')
