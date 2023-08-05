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
Rattail -> Rattail "versions" data import
"""

from rattail.importing import versions as base


class CoreposVersionMixin(object):
    """
    Add default registration of custom importers
    """

    def add_corepos_importers(self, importers):
        importers['CorePerson'] = CorePersonImporter
        importers['CoreCustomer'] = CoreCustomerImporter
        importers['CoreMember'] = CoreMemberImporter
        importers['CoreDepartment'] = CoreDepartmentImporter
        importers['CoreSubdepartment'] = CoreSubdepartmentImporter
        importers['CoreVendor'] = CoreVendorImporter
        importers['CoreProduct'] = CoreProductImporter
        return importers


class CorePersonImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CorePerson


class CoreCustomerImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreCustomer


class CoreMemberImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreMember


class CoreDepartmentImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreDepartment


class CoreSubdepartmentImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreSubdepartment


class CoreVendorImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreVendor


class CoreProductImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreProduct
