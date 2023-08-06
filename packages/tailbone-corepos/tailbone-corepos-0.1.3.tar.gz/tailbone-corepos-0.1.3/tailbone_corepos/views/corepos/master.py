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
CORE POS master view
"""

from rattail.util import OrderedDict
from rattail.time import localtime
from rattail_corepos.config import core_office_url

from webhelpers2.html import tags

from tailbone.views import MasterView
from tailbone_corepos.db import CoreOfficeSession, ExtraCoreOfficeSessions


class CoreOfficeMasterView(MasterView):
    """
    Master base class for CORE-POS views
    """
    supports_multiple_engines = True
    engine_type_key = 'corepos'
    has_local_times = True

    labels = {
        'id': "ID",
    }

    def get_db_engines(self):
        engines = OrderedDict()
        if self.rattail_config.corepos_engine:
            engines['default'] = self.rattail_config.corepos_engine
        for dbkey in sorted(self.rattail_config.corepos_engines):
            if dbkey != 'default':
                engines[dbkey] = self.rattail_config.corepos_engines[dbkey]
        return engines

    @property
    def Session(self):
        """
        Which session we return will depend on user's "current" engine.
        """
        dbkey = self.get_current_engine_dbkey()

        if dbkey != 'default' and dbkey in ExtraCoreOfficeSessions:
            return ExtraCoreOfficeSessions[dbkey]

        return CoreOfficeSession

    def make_isolated_session(self):
        from corepos.db.office_op import Session as CoreSession
        return CoreSession()

    def render_local_date(self, obj, field):
        value = getattr(obj, field)
        if not value:
            return ""
        value = localtime(self.rattail_config, value)
        return str(value.date())

    def render_corepos_department(self, obj, field):
        department = getattr(obj, field)
        if not department:
            return ""
        text = "({}) {}".format(department.number, department.name)
        url = self.request.route_url('corepos.departments.view', number=department.number)
        return tags.link_to(text, url)

    def render_corepos_vendor(self, obj, field):
        vendor = getattr(obj, field)
        if not vendor:
            return ""
        text = "({}) {}".format(vendor.abbreviation, vendor.name)
        url = self.request.route_url('corepos.vendors.view', id=vendor.id)
        return tags.link_to(text, url)

    def render_corepos_product(self, obj, field):
        product = getattr(obj, field)
        if not product:
            return ""
        text = str(product)
        url = self.request.route_url('corepos.products.view', id=product.id)
        return tags.link_to(text, url)

    def template_kwargs_view(self, **kwargs):
        """
        Adds the URL for viewing the record/object within CORE Office, or else
        the reason for lack of such a URL.
        """
        obj = kwargs['instance']

        # CORE Office URL
        kwargs['core_office_url'] = None
        office_url = core_office_url(self.rattail_config)
        if not office_url:
            kwargs['core_office_why_no_url'] = "CORE Office URL is not configured"
        else:
            url = self.core_office_object_url(office_url, obj)
            if url:
                kwargs['core_office_url'] = url
            else:
                kwargs['core_office_why_no_url'] = "URL not defined for this object"

        return kwargs

    def core_office_object_url(self, office_url, obj):
        """
        Subclass must define this logic; should return the "final" CORE Office
        URL for the given object.
        """
