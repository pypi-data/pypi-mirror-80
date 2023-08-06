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
Product Views
"""

from rattail_corepos.config import core_office_url

from tailbone.views import products as base


class ProductView(base.ProductsView):
    """
    Master view for the Product class.
    """
    labels = {
        'corepos_id': "CORE-POS ID",
    }

    @property
    def form_fields(self):
        fields = super(ProductView, self).form_fields
        return fields + [
            'corepos_id',
        ]

    def query(self, session):
        query = super(ProductView, self).query(session)
        model = self.rattail_config.get_model()
        return query.outerjoin(model.CoreProduct)

    def configure_grid(self, g):
        super(ProductView, self).configure_grid(g)
        model = self.rattail_config.get_model()
        g.set_filter('corepos_id', model.CoreProduct.corepos_id)

    def configure_form(self, f):
        super(ProductView, self).configure_form(f)

        f.set_required('corepos_id', False)
        if self.creating:
            f.remove('corepos_id')

    def objectify(self, form, data=None):
        if data is None:
            data = form.validated
        product = super(ProductView, self).objectify(form, data)

        # remove the corepos extension record outright, if we just lost the ID
        if product._corepos and not product.corepos_id:
            self.Session.delete(product._corepos)
            self.Session.flush()

        return product

    def get_version_child_classes(self):
        model = self.rattail_config.get_model()
        return super(ProductView, self).get_version_child_classes() + [
            model.CoreProduct,
        ]

    def template_kwargs_view(self, **kwargs):
        """
        Supplements the default logic as follows:

        Adds the URL for viewing the product within CORE Office, or else the
        reason for lack of such a URL.
        """
        kwargs = super(ProductView, self).template_kwargs_view(**kwargs)
        product = kwargs['instance']

        # CORE Office URL
        kwargs['core_office_url'] = None
        office_url = core_office_url(self.rattail_config)
        if not office_url:
            kwargs['core_office_why_no_url'] = "CORE Office URL is not configured"
        else:
            kwargs['core_office_url'] = '{}/item/ItemEditorPage.php?searchupc={}'.format(
                office_url, product.item_id)

        return kwargs


def includeme(config):

    # TODO: getting pretty tired of copy/pasting this extra config...
    config.add_route('products.autocomplete', '/products/autocomplete')
    config.add_view(base.ProductsAutocomplete, route_name='products.autocomplete',
                    renderer='json', permission='products.list')

    # TODO: getting pretty tired of copy/pasting this extra config...
    config.add_route('products.print_labels', '/products/labels')
    config.add_view(base.print_labels, route_name='products.print_labels',
                    renderer='json', permission='products.print_labels')

    ProductView.defaults(config)
