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
CORE-POS -> CORE-POS data import
"""

from corepos.db.office_op import Session as CoreSession

from rattail.importing.handlers import FromSQLAlchemyHandler, ToSQLAlchemyHandler
from rattail.importing.sqlalchemy import FromSQLAlchemySameToSame
from rattail.util import OrderedDict
from rattail_corepos.corepos.importing import db as corepos_importing


class FromCoreHandler(FromSQLAlchemyHandler):
    """
    Base class for import handlers which use a CORE database as the host / source.
    """
    host_title = "CORE"

    def make_host_session(self):
        return CoreSession()


class ToCoreHandler(ToSQLAlchemyHandler):
    """
    Base class for import handlers which target a CORE database on the local side.
    """
    local_title = "CORE"

    def make_session(self):
        return CoreSession()


class FromCoreToCoreBase(object):
    """
    Common base class for Core -> Core data import/export handlers.
    """

    def get_importers(self):
        importers = OrderedDict()
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Vendor'] = VendorImporter
        importers['VendorContact'] = VendorContactImporter
        importers['Product'] = ProductImporter
        importers['ProductFlag'] = ProductFlagImporter
        importers['Employee'] = EmployeeImporter
        importers['CustData'] = CustDataImporter
        importers['MemberType'] = MemberTypeImporter
        importers['MemberInfo'] = MemberInfoImporter
        importers['HouseCoupon'] = HouseCouponImporter
        return importers


class FromCoreToCoreImport(FromCoreToCoreBase, FromCoreHandler, ToCoreHandler):
    """
    Handler for CORE (other) -> CORE (local) data import.

    .. attribute:: direction

       Value is ``'import'`` - see also
       :attr:`rattail.importing.handlers.ImportHandler.direction`.
    """
    dbkey = 'host'
    local_title = "CORE (default)"

    @property
    def host_title(self):
        return "CORE ({})".format(self.dbkey)

    def make_host_session(self):
        return CoreSession(bind=self.config.corepos_engines[self.dbkey])


class FromCoreToCoreExport(FromCoreToCoreBase, FromCoreHandler, ToCoreHandler):
    """
    Handler for CORE (local) -> CORE (other) data export.

    .. attribute:: direction

       Value is ``'export'`` - see also
       :attr:`rattail.importing.handlers.ImportHandler.direction`.
    """
    direction = 'export'
    host_title = "CORE (default)"

    @property
    def local_title(self):
        return "CORE ({})".format(self.dbkey)

    def make_session(self):
        return CoreSession(bind=self.config.corepos_engines[self.dbkey])


class FromCore(FromSQLAlchemySameToSame):
    """
    Base class for CORE -> CORE data importers.
    """


class DepartmentImporter(FromCore, corepos_importing.model.DepartmentImporter):
    pass

class SubdepartmentImporter(FromCore, corepos_importing.model.SubdepartmentImporter):
    pass

class VendorImporter(FromCore, corepos_importing.model.VendorImporter):
    pass

class VendorContactImporter(FromCore, corepos_importing.model.VendorContactImporter):
    pass

class ProductImporter(FromCore, corepos_importing.model.ProductImporter):
    pass

class ProductFlagImporter(FromCore, corepos_importing.model.ProductFlagImporter):
    pass

class EmployeeImporter(FromCore, corepos_importing.model.EmployeeImporter):
    pass

class CustDataImporter(FromCore, corepos_importing.model.CustDataImporter):
    pass

class MemberTypeImporter(FromCore, corepos_importing.model.MemberTypeImporter):
    pass

class MemberInfoImporter(FromCore, corepos_importing.model.MemberInfoImporter):
    pass

class HouseCouponImporter(FromCore, corepos_importing.model.HouseCouponImporter):
    pass
