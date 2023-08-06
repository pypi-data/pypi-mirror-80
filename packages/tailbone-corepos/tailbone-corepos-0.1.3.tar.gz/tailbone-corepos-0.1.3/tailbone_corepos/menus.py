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
Common menus for CORE-POS
"""

from rattail_corepos.config import core_office_url


def make_corepos_menu(request):
    url = request.route_url

    corepos_menu = {
        'title': "CORE-POS",
        'type': 'menu',
        'items': [
            {
                'title': "Customers (Legacy)",
                'url': url('corepos.customers'),
                'perm': 'corepos.customers.list',
            },
            {
                'title': "Members (Legacy)",
                'url': url('corepos.members'),
                'perm': 'corepos.members.list',
            },
            {
                'title': "Member Types",
                'url': url('corepos.member_types'),
                'perm': 'corepos.member_types.list',
            },
            {
                'title': "Employees",
                'url': url('corepos.employees'),
                'perm': 'corepos.employees.list',
            },
            {'type': 'sep'},
            {
                'title': "Products",
                'url': url('corepos.products'),
                'perm': 'corepos.products.list',
            },
            {
                'title': "Scale Items",
                'url': url('corepos.scale_items'),
                'perm': 'corepos.scale_items.list',
            },
            {
                'title': "Super Departments",
                'url': url('corepos.super_departments'),
                'perm': 'corepos.super_departments.list',
            },
            {
                'title': "Departments",
                'url': url('corepos.departments'),
                'perm': 'corepos.departments.list',
            },
            {
                'title': "Subdepartments",
                'url': url('corepos.subdepartments'),
                'perm': 'corepos.subdepartments.list',
            },
            {
                'title': "Vendors",
                'url': url('corepos.vendors'),
                'perm': 'corepos.vendors.list',
            },
            {
                'title': "Origins",
                'url': url('corepos.origins'),
                'perm': 'corepos.origins.list',
            },
            {'type': 'sep'},
            {
                'title': "Batches",
                'url': url('corepos.batches'),
                'perm': 'corepos.batches.list',
            },
            {
                'title': "Batch Types",
                'url': url('corepos.batch_types'),
                'perm': 'corepos.batch_types.list',
            },
            # {'type': 'sep'},
            # {
            #     'title': "Transaction Details",
            #     'url': url('corepos.transaction_details'),
            #     'perm': 'corepos.transaction_details.list',
            # },
        ],
    }

    office_url = core_office_url(request.rattail_config)
    if office_url:
        corepos_menu['items'].extend([
            {'type': 'sep'},
            {
                'title': "Go to CORE Office",
                'url': '{}/'.format(office_url),
                'target': '_blank',
            },
        ])

    return corepos_menu
