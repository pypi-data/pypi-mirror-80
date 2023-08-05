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
Rattail -> CORE-POS data export
"""

import logging

from sqlalchemy import orm

from rattail import importing
from rattail.db import model
from rattail.db.util import short_session
from rattail.util import OrderedDict
from rattail_corepos.corepos import importing as corepos_importing
from rattail_corepos.corepos.util import get_max_existing_vendor_id


log = logging.getLogger(__name__)


class FromRattailToCore(importing.FromRattailHandler):
    """
    Rattail -> CORE-POS export handler
    """
    host_title = "Rattail"
    local_title = "CORE-POS"
    direction = 'export'

    def get_importers(self):
        importers = OrderedDict()
        importers['Member'] = MemberImporter
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Vendor'] = VendorImporter
        importers['Product'] = ProductImporter
        return importers


class FromRattail(importing.FromSQLAlchemy):
    """
    Base class for Rattail -> CORE-POS exporters.
    """


class MemberImporter(FromRattail, corepos_importing.model.MemberImporter):
    """
    Member data exporter
    """
    host_model_class = model.Customer
    key = 'cardNo'
    supported_fields = [
        'cardNo',
        'customerAccountID',
        'customers',
        'addressFirstLine',
        'addressSecondLine',
        'city',
        'state',
        'zip',
        'startDate',
        'endDate',
    ]
    supported_customer_fields = [
        'customerID',
        'firstName',
        'lastName',
        'accountHolder',
        'phone',
        'altPhone',
        'email',
    ]

    def query(self):
        query = super(MemberImporter, self).query()
        query = query.options(orm.joinedload(model.Customer.addresses))\
                .options(orm.joinedload(model.Customer._people)\
                         .joinedload(model.CustomerPerson.person)\
                         .joinedload(model.Person.phones))\
                .options(orm.joinedload(model.Customer._people)\
                         .joinedload(model.CustomerPerson.person)\
                         .joinedload(model.Person.emails))
        return query

    def normalize_host_object(self, customer):

        address = customer.addresses[0] if customer.addresses else None

        people = []
        for i, person in enumerate(customer.people, 1):
            phones = person.phones
            phone1 = phones[0] if phones else None
            phone2 = phones[1] if len(phones) > 1 else None
            email = person.emails[0] if person.emails else None
            people.append({
                'customerID': str(person.corepos_customer_id),
                'firstName': person.first_name,
                'lastName': person.last_name,
                'accountHolder': i == 1,
                'phone': phone1.number if phone1 else '',
                'altPhone': phone2.number if phone2 else '',
                'email': email.address if email else '',
            })

        member = customer.only_member(require=False)
        if member:
            if member.joined:
                start_date = member.joined.strftime('%Y-%m-%d 00:00:00')
            else:
                start_date = self.empty_date_value
            if member.withdrew:
                end_date = member.withdrew.strftime('%Y-%m-%d 00:00:00')
            else:
                end_date = self.empty_date_value
        else:
            start_date = '__omit__'
            end_date = '__omit__'

        return {
            'cardNo': customer.number,
            'customerAccountID': customer.id,
            'addressFirstLine': address.street if address else '',
            'addressSecondLine': address.street2 if address else '',
            'city': address.city if address else '',
            'state': address.state if address else '',
            'zip': address.zipcode if address else '',
            'startDate': start_date,
            'endDate': end_date,
            'customers': people,
        }


class DepartmentImporter(FromRattail, corepos_importing.model.DepartmentImporter):
    """
    Department data exporter
    """
    host_model_class = model.Department
    key = 'dept_no'
    supported_fields = [
        'dept_no',
        'dept_name',
    ]

    def normalize_host_object(self, department):
        return {
            'dept_no': str(department.number),
            'dept_name': department.name,
        }


class SubdepartmentImporter(FromRattail, corepos_importing.model.SubdepartmentImporter):
    """
    Subdepartment data exporter
    """
    host_model_class = model.Subdepartment
    key = 'subdept_no'
    supported_fields = [
        'subdept_no',
        'subdept_name',
        'dept_ID',
    ]

    def normalize_host_object(self, subdepartment):
        department = subdepartment.department
        return {
            'subdept_no': str(subdepartment.number),
            'subdept_name': subdepartment.name,
            'dept_ID': str(department.number) if department else None,
        }


class VendorImporter(FromRattail, corepos_importing.model.VendorImporter):
    """
    Vendor data exporter
    """
    host_model_class = model.Vendor
    key = 'vendorID'
    supported_fields = [
        'vendorID',
        'vendorName',
        'vendorAbbreviation',
        'discountRate',
        'phone',
        'fax',
        'email',
    ]

    def setup(self):
        super(VendorImporter, self).setup()

        # self.max_existing_vendor_id = self.get_max_existing_vendor_id()
        self.max_existing_vendor_id = get_max_existing_vendor_id()
        self.last_vendor_id = self.max_existing_vendor_id

    def get_next_vendor_id(self):
        if hasattr(self, 'last_vendor_id'):
            self.last_vendor_id += 1
            return self.last_vendor_id

        last_vendor_id = get_max_existing_vendor_id()
        return last_vendor_id + 1

    def normalize_host_object(self, vendor):
        vendor_id = vendor.corepos_id
        if not vendor_id:
            vendor_id = self.get_next_vendor_id()

        data = {
            'vendorID': str(vendor_id),
            'vendorName': vendor.name,
            'vendorAbbreviation': vendor.abbreviation or '',
            'discountRate': float(vendor.special_discount or 0),
        }

        if 'phone' in self.fields:
            phones = [phone for phone in vendor.phones
                      if phone.type == 'Voice']
            data['phone'] = phones[0].number if phones else ''

        if 'fax' in self.fields:
            phones = [phone for phone in vendor.phones
                      if phone.type == 'Fax']
            data['fax'] = phones[0].number if phones else ''

        if 'email' in self.fields:
            email = vendor.email
            data['email'] = email.address if email else ''

        # also embed original Rattail vendor object, if we'll be needing to
        # update it later with a new CORE ID
        if not vendor.corepos_id:
            data['_rattail_vendor'] = vendor

        return data

    def create_object(self, key, data):

        # grab vendor object we (maybe) stashed when normalizing
        rattail_vendor = data.pop('_rattail_vendor', None)

        # do normal create logic
        vendor = super(VendorImporter, self).create_object(key, data)
        if vendor:

            # maybe set the CORE ID for vendor in Rattail
            if rattail_vendor:
                rattail_vendor.corepos_id = int(vendor['vendorID'])

            return vendor


class ProductImporter(FromRattail, corepos_importing.model.ProductImporter):
    """
    Product data exporter
    """
    host_model_class = model.Product
    key = 'upc'
    supported_fields = [
        'upc',
        'brand',
        'description',
        'size',
        'department',
        'normal_price',
        'foodstamp',
        'scale',
    ]

    def normalize_host_object(self, product):
        upc = product.item_id
        if not upc and product.upc:
            upc = str(product.upc)[:-1]
        if not upc:
            log.warning("skipping product %s with unknown upc: %s",
                        product.uuid, product)
            return

        return {
            '_product': product,
            'upc': upc,
            'brand': product.brand.name if product.brand else '',
            'description': product.description or '',
            'size': product.size or '',
            'department': str(product.department.number) if product.department else None,
            'normal_price': '{:0.2f}'.format(product.regular_price.price) if product.regular_price else None,
            'foodstamp': '1' if product.food_stampable else '0',
            'scale': '1' if product.weighed else '0',
        }

    def create_object(self, key, data):

        # must be sure not to pass the original Product instance, or else the
        # API call will try to serialize and submit it
        product = data.pop('_product')

        corepos_product = super(ProductImporter, self).create_object(key, data)
        if corepos_product:

            # update our Rattail Product with the CORE ID
            if not self.dry_run:
                product.corepos_id = int(corepos_product['id'])
                return corepos_product

    def update_object(self, corepos_product, data, local_data=None):

        # must be sure not to pass the original Product instance, or else the
        # API call will try to serialize and submit it
        product = data.pop('_product', None)

        corepos_product = super(ProductImporter, self).update_object(corepos_product, data, local_data)
        return corepos_product
