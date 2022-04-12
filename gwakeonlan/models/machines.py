##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from gwakeonlan.constants import BROADCAST_ADDRESS
from gwakeonlan.models.abstract import ModelAbstract


class ModelMachines(ModelAbstract):
    COL_SELECTED = 1
    COL_MACADDRESS = 2
    COL_REQUESTTYPE = 3
    COL_DESTINATION = 4
    COL_PORTNR = 5
    COL_ICON = 6

    def add_data(self, item):
        """Add a new row to the model if it doesn't exist"""
        super(self.__class__, self).add_data(item)
        if item.name not in self.rows:
            new_row = self.model.append((
                item.name,
                False,
                item.mac_address.upper(),
                'Local'
                if item.destination == BROADCAST_ADDRESS
                else 'Internet',
                item.destination,
                item.port_number,
                item.icon
            ))
            self.rows[item.name] = new_row

    def get_selected(self, treeiter):
        """Return if the TreeIter is selected"""
        return self.get_model_data(treeiter, self.__class__.COL_SELECTED)

    def set_selected(self, treeiter, value):
        """Set the TreeIter selection"""
        self.set_model_data(treeiter, self.__class__.COL_SELECTED, value)

    def get_machine_name(self, treeiter):
        """Return the machine name from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_KEY)

    def set_machine_name(self, treeiter, value):
        """Set the machine name for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_KEY, value)

    def get_mac_address(self, treeiter):
        """Return the MAC address from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_MACADDRESS)

    def set_mac_address(self, treeiter, value):
        """Set the MAC address for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_MACADDRESS, value)

    def get_request_type(self, treeiter):
        """Return the request type from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_REQUESTTYPE)

    def get_destination(self, treeiter):
        """Return the destination from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_DESTINATION)

    def set_destination(self, treeiter, value):
        """Set the destination for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_DESTINATION, value)
        self.set_model_data(treeiter, self.__class__.COL_REQUESTTYPE,
                            'Local'
                            if value == BROADCAST_ADDRESS
                            else 'Internet')

    def get_port_number(self, treeiter):
        """Return the port number from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_PORTNR)

    def set_port_number(self, treeiter, value):
        """Set the port number for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_PORTNR, value)

    def set_icon(self, treeiter, value):
        """Set the background color for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_ICON, value)
