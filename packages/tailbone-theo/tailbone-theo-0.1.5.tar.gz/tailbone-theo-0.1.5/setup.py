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
Theo setup script
"""

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'theo', '_version.py')).read())
README = open(os.path.join(here, 'README.rst')).read()


requires = [
    #
    # Version numbers within comments below have specific meanings.
    # Basically the 'low' value is a "soft low," and 'high' a "soft high."
    # In other words:
    #
    # If either a 'low' or 'high' value exists, the primary point to be
    # made about the value is that it represents the most current (stable)
    # version available for the package (assuming typical public access
    # methods) whenever this project was started and/or documented.
    # Therefore:
    #
    # If a 'low' version is present, you should know that attempts to use
    # versions of the package significantly older than the 'low' version
    # may not yield happy results.  (A "hard" high limit may or may not be
    # indicated by a true version requirement.)
    #
    # Similarly, if a 'high' version is present, and especially if this
    # project has laid dormant for a while, you may need to refactor a bit
    # when attempting to support a more recent version of the package.  (A
    # "hard" low limit should be indicated by a true version requirement
    # when a 'high' version is present.)
    #
    # In any case, developers and other users are encouraged to play
    # outside the lines with regard to these soft limits.  If bugs are
    # encountered then they should be filed as such.
    #
    # package                           # low                   high

]


extras = {

    'app': [
        #
        # package                       # low                   high

        'invoke',                       # 1.4.1
        'psycopg2',                     # 2.8.5
        'rattail[db,auth,bouncer]',     # 0.9.130
        'Tailbone',                     # 0.8.97
    ],

    'catapult': [
        #
        # package                       # low                   high

        # TODO: must cap this for now, b/c it breaks Catapult integration?!
        # (something about "Syntax error near 'ROWS'" with grid queries)
        'SQLAlchemy<1.3',               #                       1.2.19

        'onager',                       # 0.2.8
        'rattail-onager',               # 0.2.1
        'tailbone-onager',              # 0.2.3
    ],

    'corepos': [
        #
        # package                       # low                   high

        # TODO: must cap this for now, b/c it breaks CORE-POS integration?!
        # (sometimes there are segfaults with basic grid queries)
        'mysql-connector-python==8.0.17',

        'pyCOREPOS',                    # 0.1.0
        'rattail-corepos',              # 0.1.0
        'tailbone-corepos',             # 0.1.1
    ],

    'fabric': [
        #
        # package                       # low                   high

        'rattail-fabric2',              # 0.2.3
    ],

    'locsms': [
        #
        # package                       # low                   high

        'luckysmores',                  # 0.2.3
        'rattail-luckysmores',          # 0.8.2
        'tailbone-locsms',              # 0.1.0
    ],
}


setup(
    name = "tailbone-theo",
    version = __version__,
    author = "Lance Edgar",
    author_email = "lance@edbob.org",
    url = "https://rattailproject.org",
    description = "Theo, the order system",
    long_description = README,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business',
    ],

    install_requires = requires,
    extras_require = extras,
    packages = find_packages(),
    include_package_data = True,

    entry_points = {

        'rattail.config.extensions': [
            'theo = theo.config:TheoConfig',
        ],

        'paste.app_factory': [
            'main = theo.web.app:main',
        ],
    },
)
