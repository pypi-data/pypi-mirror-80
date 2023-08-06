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
CORE POS customer views
"""

from corepos.db.office_op import model as corepos

from rattail_corepos.config import core_office_customer_account_url

from webhelpers2.html import tags

from .master import CoreOfficeMasterView


class CustomerView(CoreOfficeMasterView):
    """
    Base class for customer views.
    """
    model_class = corepos.CustData
    model_title = "CORE-POS Customer (Legacy)"
    model_title_plural = "CORE-POS Customers (Legacy)"
    url_prefix = '/core-pos/customers'
    route_prefix = 'corepos.customers'

    labels = {
        'id': "ID",
        'card_number': "Card No.",
        'person_number': "Person No.",
        'charge_ok': "Charge OK",
        'member_type_id': "Member Type No.",
        'number_of_checks': "Number of Checks",
        'ssi': "SSI",
    }

    grid_columns = [
        'card_number',
        'person_number',
        'first_name',
        'last_name',
        'member_type',
        'ssi',
        'charge_ok',
        'charge_limit',
        'balance',
        'write_checks',
        'purchases',
    ]

    def configure_grid(self, g):
        super(CustomerView, self).configure_grid(g)

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'

        g.filters['first_name'].default_active = True
        g.filters['first_name'].default_verb = 'contains'

        g.filters['last_name'].default_active = True
        g.filters['last_name'].default_verb = 'contains'

        g.set_joiner('member_type', lambda q: q.outerjoin(corepos.MemberType))
        g.set_sorter('member_type', corepos.MemberType.description)
        g.set_filter('member_type', corepos.MemberType.description)

        g.set_type('charge_limit', 'currency')
        g.set_type('balance', 'currency')
        g.set_type('purchases', 'currency')

        g.set_sort_defaults('card_number')

        g.set_link('card_number')
        g.set_link('first_name')
        g.set_link('last_name')

    def configure_form(self, f):
        super(CustomerView, self).configure_form(f)

        f.set_renderer('member_info', self.render_member_info)
        f.set_renderer('member_type', self.render_member_type)

        if self.creating or self.editing:
            f.remove_field('member_info')
            f.remove_field('member_type')
            f.remove_field('last_change')
        else:
            f.set_type('last_change', 'datetime_local')

    def render_member_type(self, custdata, field):
        memtype = custdata.member_type
        if not memtype:
            return
        text = str(memtype)
        url = self.request.route_url('corepos.member_types.view', id=memtype.id)
        return tags.link_to(text, url)

    def render_member_info(self, custdata, field):
        meminfo = custdata.member_info
        if not meminfo:
            return
        text = str(meminfo)
        url = self.request.route_url('corepos.members.view',
                                     card_number=meminfo.card_number)
        return tags.link_to(text, url)

    def core_office_object_url(self, office_url, customer):
        return core_office_customer_account_url(self.rattail_config,
                                                customer.card_number,
                                                office_url=office_url)


def includeme(config):
    CustomerView.defaults(config)
