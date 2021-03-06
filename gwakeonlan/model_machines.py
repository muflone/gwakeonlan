##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2020 Fabio Castelli
#     License: GPL-3+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

from gi.repository import Gtk

from gwakeonlan.constants import BROADCAST_ADDRESS


class ModelMachines(object):
    COL_SELECTED = 0
    COL_MACHINE = 1
    COL_MACADDRESS = 2
    COL_REQUESTTYPE = 3
    COL_DESTINATION = 4
    COL_PORTNR = 5

    def __init__(self, model):
        """Initialize the model"""
        self.model = model
        self.index = 0

    def path_from_iter(self, treeiter):
        """Return a TreePath from a TreeIter"""
        return type(treeiter) is Gtk.TreeModelRow and treeiter.path or treeiter

    def get_model_data(self, treeiter, column):
        """Get model data from a TreeIter column"""
        return self.model[self.path_from_iter(treeiter)][column]

    def set_model_data(self, treeiter, column, value):
        """Set model data for a TreeIter column"""
        self.model[self.path_from_iter(treeiter)][column] = value

    def get_selected(self, treeiter):
        """Return if the TreeIter is selected"""
        return self.get_model_data(treeiter, self.__class__.COL_SELECTED)

    def set_selected(self, treeiter, value):
        """Set the TreeIter selection"""
        self.set_model_data(treeiter, self.__class__.COL_SELECTED, value)

    def get_machine_name(self, treeiter):
        """Return the machine name from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_MACHINE)

    def set_machine_name(self, treeiter, value):
        """Set the machine name for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_MACHINE, value)

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
                            value == BROADCAST_ADDRESS and 'Local' or
                            'Internet')

    def get_portnr(self, treeiter):
        """Return the port number from a TreeIter"""
        return self.get_model_data(treeiter, self.__class__.COL_PORTNR)

    def set_portnr(self, treeiter, value):
        """Set the port number for a TreeIter"""
        self.set_model_data(treeiter, self.__class__.COL_PORTNR, value)

    def add_machine(self, selected, machine_name, mac_address, portnr,
                    destination):
        """Add a new machine to the model"""
        return self.model.append((
            selected,
            machine_name,
            mac_address,
            destination == BROADCAST_ADDRESS and 'Local' or 'Internet',
            destination,
            portnr
        ))

    def remove(self, treeiter):
        """Remove a machine from the model"""
        self.model.remove(treeiter)

    def clear(self):
        """Clear the model"""
        return self.model.clear()

    def count(self):
        """Return the number of items in the model"""
        return len(self.model)

    def __iter__(self):
        """Iter the model"""
        return iter(self.model)
