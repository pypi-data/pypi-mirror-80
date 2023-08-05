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
Rattail model importer extensions, for CORE-POS integration
"""

from rattail import importing


##############################
# core importer overrides
##############################

class PersonImporter(importing.model.PersonImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_customer_id',
    ]

    def cache_query(self):
        query = super(PersonImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore people with no CORE ID, if that's (part of) our key
        if 'corepos_customer_id' in self.key:
            query = query.join(model.CorePerson)\
                         .filter(model.CorePerson.corepos_customer_id != None)

        return query


class CustomerImporter(importing.model.CustomerImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_account_id',
    ]


class MemberImporter(importing.model.MemberImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_account_id',
    ]


class DepartmentImporter(importing.model.DepartmentImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_number',
    ]


class SubdepartmentImporter(importing.model.SubdepartmentImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_number',
    ]


class VendorImporter(importing.model.VendorImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_id',
    ]


class ProductImporter(importing.model.ProductImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_id',
    ]

    def cache_query(self):
        query = super(ProductImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore products with no CORE ID, if that's (part of) our key
        if 'corepos_id' in self.key:
            query = query.join(model.CoreProduct)\
                         .filter(model.CoreProduct.corepos_id != None)

        return query


class ProductCostImporter(importing.model.ProductCostImporter):

    extension_attr = '_corepos'
    extension_fields = [
        'corepos_id',
    ]

    def cache_query(self):
        query = super(ProductCostImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore items with no CORE ID, if that's (part of) our key
        if 'corepos_id' in self.key:
            query = query.join(model.CoreProductCost)\
                         .filter(model.CoreProductCost.corepos_id != None)

        return query
