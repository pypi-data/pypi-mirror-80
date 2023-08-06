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
CORE-POS product views
"""

from corepos.db.office_op import model as corepos
from corepos.db.util import table_exists

from webhelpers2.html import HTML

from .master import CoreOfficeMasterView


class ProductView(CoreOfficeMasterView):
    """
    Base class for product views.
    """
    model_class = corepos.Product
    model_title = "CORE-POS Product"
    url_prefix = '/core-pos/products'
    route_prefix = 'corepos.products'
    results_downloadable = True

    labels = {
        'id': "ID",
        'upc': "UPC",
        'department_number': "Dept. No.",
        'foodstamp': "Food Stamp",
        'unit_of_measure': "Unit of Measure",
        'quantity_enforced': "Qty. Enforced",
        'id_enforced': "ID Enforced",
        'subdepartment_number': "Subdept. No.",
        'default_vendor_id': "Default Vendor ID",
        'current_origin_id': "Current Origin ID",
    }

    grid_columns = [
        'upc',
        'brand',
        'description',
        'size',
        'department',
        'vendor',
        'normal_price',
        'cost',
    ]

    def configure_grid(self, g):
        super(ProductView, self).configure_grid(g)

        g.set_joiner('department', lambda q: q.outerjoin(corepos.Department))
        g.set_sorter('department', corepos.Department.name)

        g.set_joiner('vendor', lambda q: q.outerjoin(corepos.Vendor,
                                                     corepos.Vendor.id == corepos.Product.default_vendor_id))
        g.set_sorter('vendor', corepos.Vendor.name)
        g.set_filter('vendor', corepos.Vendor.name)

        g.filters['upc'].default_active = True
        g.filters['upc'].default_verb = 'contains'

        g.set_type('cost', 'currency')
        g.set_type('normal_price', 'currency')

        g.set_sort_defaults('upc')

        g.set_link('upc')
        g.set_link('brand')
        g.set_link('description')

    def configure_form(self, f):
        super(ProductView, self).configure_form(f)

        if not table_exists(self.Session(), corepos.FloorSection):
            f.remove('physical_location')

        f.set_renderer('vendor', self.render_corepos_vendor)

        f.set_renderer('flags', self.render_flags)

        f.set_type('start_date', 'datetime_local')
        f.set_type('end_date', 'datetime_local')
        f.set_type('last_sold', 'datetime_local')
        f.set_type('modified', 'datetime_local')

        f.set_type('normal_price', 'currency')
        f.set_type('group_price', 'currency')
        f.set_type('special_price', 'currency')
        f.set_type('special_group_price', 'currency')
        f.set_type('cost', 'currency')
        f.set_type('deposit', 'currency')

    def render_flags(self, product, field):
        flags = product.flags
        if not flags:
            return ""

        # fetch all flags which are actually defined (supported)
        supported = {}
        for flag in self.Session.query(corepos.ProductFlag):
            supported[flag.bit_number] = flag

        # convert product's flag value to string of bits
        bflags = bin(flags)[2:]   # remove '0b' prefix
        bflags = reversed(bflags) # make bit #1 first in string, etc.

        # create list of items to show each "set" flag
        items = []
        for i, bit in enumerate(bflags, 1):
            if bit == '1':
                flag = supported.get(i)
                if flag:
                    items.append(HTML.tag('li', c=flag.description))
                else:
                    items.append(HTML.tag('li', c="(unsupported bit #{})".format(i)))

        return HTML.tag('ul', c=items)

    def core_office_object_url(self, office_url, product):
        return '{}/item/ItemEditorPage.php?searchupc={}'.format(
            office_url, product.upc)

    def download_results_fields_available(self, **kwargs):
        fields = super(ProductView, self).download_results_fields_available(**kwargs)

        fields.append('superdepartment_number')

        return fields

    def download_results_setup(self, fields, progress=None):
        super(ProductView, self).download_results_setup(fields, progress=progress)

        if 'superdepartment_number' in fields:
            mapping = {}
            super_departments = self.Session.query(corepos.SuperDepartment).all()
            for superdept in super_departments:
                if superdept.child_id in mapping:
                    if superdept.parent_id < mapping[superdept.child_id]:
                        mapping[superdept.child_id] = superdept.parent_id
                else:
                    mapping[superdept.child_id] = superdept.parent_id
            self.supermap = mapping

    def download_results_normalize(self, product, fields, **kwargs):
        data = super(ProductView, self).download_results_normalize(product, fields, **kwargs)

        if 'superdepartment_number' in fields:
            data['superdepartment_number'] = None
            if product.department_number in self.supermap:
                data['superdepartment_number'] = self.supermap[product.department_number]

        return data


class ProductFlagView(CoreOfficeMasterView):
    """
    Master view for product flags
    """
    model_class = corepos.ProductFlag
    model_title = "CORE-POS Product Flag"
    url_prefix = '/core-pos/product-flags'
    route_prefix = 'corepos.product_flags'

    def configure_grid(self, g):
        super(ProductFlagView, self).configure_grid(g)

        g.set_link('bit_number')
        g.set_link('description')

    def grid_extra_class(self, flag, i):
        if not flag.active:
            return 'warning'


def includeme(config):
    ProductView.defaults(config)
    ProductFlagView.defaults(config)
