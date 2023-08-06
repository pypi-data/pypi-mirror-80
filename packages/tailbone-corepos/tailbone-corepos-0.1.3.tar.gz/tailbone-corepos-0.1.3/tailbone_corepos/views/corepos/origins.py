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
CORE-POS origin views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class OriginView(CoreOfficeMasterView):
    """
    Base class for origin views.
    """
    model_class = corepos.Origin
    model_title = "CORE-POS Origin"
    url_prefix = '/core-pos/origins'
    route_prefix = 'corepos.origins'

    labels = {
        'country_id': "Country ID",
        'state_prov_id': "State/Province ID",
        'state_prov': "State/Province",
        'custom_id': "Custom Region ID",
    }

    grid_columns = [
        'id',
        'name',
        'short_name',
        'local',
        'country',
        'state_prov',
        'custom_region',
    ]

    form_fields = [
        'id',
        'name',
        'short_name',
        'local',
        'country',
        'state_prov',
        'custom_region',
    ]


def includeme(config):
    OriginView.defaults(config)
