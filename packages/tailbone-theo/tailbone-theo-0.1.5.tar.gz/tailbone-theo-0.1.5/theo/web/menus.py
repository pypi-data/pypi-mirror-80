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
Web Menus
"""

from theo.config import integrate_catapult, integrate_corepos, integrate_locsms


def simple_menus(request):
    url = request.route_url
    rattail_config = request.rattail_config

    include_catapult = integrate_catapult(rattail_config)
    include_corepos = integrate_corepos(rattail_config)
    include_locsms = integrate_locsms(rattail_config)

    orders_menu = {
        'title': "Orders",
        'type': 'menu',
        'items': [
            {
                'title': "New Customer Order",
                'url': url('custorders.create'),
                'perm': 'custorders.create',
            },
            {
                'title': "All New Orders",
                'url': url('new_custorders'),
                'perm': 'new_custorders.list',
            },
            {'type': 'sep'},
            {
                'title': "All Customer Orders",
                'url': url('custorders'),
                'perm': 'custorders.list',
            },
            {
                'title': "All Order Items",
                'url': url('custorders.items'),
                'perm': 'custorders.items.list',
            },
            # {
            #     'title': "Configuration",
            #     'url': url('custorders.config'),
            #     'perm': 'custorders.configure',
            # },
        ],
    }

    people_menu = {
        'title': "People",
        'type': 'menu',
        'items': [
            {
                'title': "Customers",
                'url': url('customers'),
                'perm': 'customers.list',
            },
            {
                'title': "Members",
                'url': url('members'),
                'perm': 'members.list',
            },
            {
                'title': "Employees",
                'url': url('employees'),
                'perm': 'employees.list',
            },
            {
                'title': "All People",
                'url': url('people'),
                'perm': 'people.list',
            },
        ],
    }

    products_menu = {
        'title': "Products",
        'type': 'menu',
        'items': [
            {
                'title': "Products",
                'url': url('products'),
                'perm': 'products.list',
            },
            {
                'title': "Departments",
                'url': url('departments'),
                'perm': 'departments.list',
            },
            {
                'title': "Subdepartments",
                'url': url('subdepartments'),
                'perm': 'subdepartments.list',
            },
            {
                'title': "Brands",
                'url': url('brands'),
                'perm': 'brands.list',
            },
            {
                'title': "Vendors",
                'url': url('vendors'),
                'perm': 'vendors.list',
            },
            {
                'title': "Taxes",
                'url': url('taxes'),
                'perm': 'taxes.list',
            },
        ],
    }

    if include_catapult:
        catapult_menu = {
            'title': "Catapult",
            'type': 'menu',
            'items': [
                {
                    'title': "Departments",
                    'url': url('catapult.departments'),
                    'perm': 'catapult.departments.list',
                },
                {
                    'title': "Terminals",
                    'url': url('catapult.terminals'),
                    'perm': 'catapult.terminals.list',
                },
                {
                    'title': "Transactions",
                    'url': url('catapult.transactions'),
                    'perm': 'catapult.transactions.list',
                },
                {
                    'title': "Worksheets",
                    'url': url('catapult.worksheets'),
                    'perm': 'catapult.worksheets.list',
                },
                {'type': 'sep'},
                {
                    'title': "Security Profiles",
                    'url': url('catapult.security_profiles'),
                    'perm': 'catapult.security_profiles.view',
                },
                {
                    'title': "Master Functions",
                    'url': url('catapult.master_functions'),
                    'perm': 'catapult.master_functions.view',
                },
            ],
        }

    if include_corepos:
        from tailbone_corepos.menus import make_corepos_menu
        corepos_menu = make_corepos_menu(request)

    if include_locsms:
        from tailbone_locsms.menus import make_locsms_menu
        locsms_menu = make_locsms_menu(request)

    admin_menu = {
        'title': "Admin",
        'type': 'menu',
        'items': [
            {
                'title': "Stores",
                'url': url('stores'),
                'perm': 'stores.list',
            },
            {
                'title': "Users",
                'url': url('users'),
                'perm': 'users.list',
            },
            {
                'title': "User Events",
                'url': url('userevents'),
                'perm': 'userevents.list',
            },
            {
                'title': "Roles",
                'url': url('roles'),
                'perm': 'roles.list',
            },
            {'type': 'sep'},
            {
                'title': "App Settings",
                'url': url('appsettings'),
                'perm': 'settings.list',
            },
            {
                'title': "Email Settings",
                'url': url('emailprofiles'),
                'perm': 'emailprofiles.list',
            },
            {
                'title': "Email Attempts",
                'url': url('email_attempts'),
                'perm': 'email_attempts.list',
            },
            {
                'title': "Raw Settings",
                'url': url('settings'),
                'perm': 'settings.list',
            },
            {'type': 'sep'},
            {
                'title': "DataSync Changes",
                'url': url('datasyncchanges'),
                'perm': 'datasync.list',
            },
            {
                'title': "Tables",
                'url': url('tables'),
                'perm': 'tables.list',
            },
            {
                'title': "Theo Upgrades",
                'url': url('upgrades'),
                'perm': 'upgrades.list',
            },
        ],
    }

    menus = [
        orders_menu,
        people_menu,
        products_menu,
    ]

    if include_catapult:
        menus.append(catapult_menu)
    if include_corepos:
        menus.append(corepos_menu)
    if include_locsms:
        menus.append(locsms_menu)

    menus.append(admin_menu)

    return menus
