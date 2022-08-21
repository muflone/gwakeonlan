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

import logging

from gi.repository import GLib
from gi.repository import Gtk

from gwakeonlan.functions import get_treeview_selected_row
from gwakeonlan.models.arpcache import ModelArpCache
from gwakeonlan.ui.base import UIBase

SECTION_WINDOW_NAME = 'arp cache'


class UIArpCache(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='arpcache.ui')
        # Initialize members
        self.parent = parent
        self.settings = settings
        self.options = options
        # Prepare the models
        self.model = ModelArpCache(self.ui.model)
        self.model.refresh()
        # Load UI
        self.load_ui()
        # Complete initialization
        self.startup()

    def load_ui(self):
        """Load the interface UI"""
        logging.debug(f'{self.__class__.__name__} load UI')
        # Initialize titles and tooltips
        self.set_titles()
        # Set various properties
        self.ui.dialog.set_transient_for(self.parent)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.dialog,
                                              section=SECTION_WINDOW_NAME)

    def destroy(self):
        """Hide and destroy the ARP cache picker dialog"""
        logging.debug(f'{self.__class__.__name__} destroy')
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def show(self):
        """Show the dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.dialog.hide)
        response = self.ui.dialog.run()
        self.ui.dialog.hide()
        return response

    def do_get_hostname(self):
        """Returns the hostname of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_hostname(treeiter)

    def do_get_ip_address(self):
        """Returns the IP address of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_ip_address(treeiter)

    def do_get_mac_address(self):
        """Returns the MAC address of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_mac_address(treeiter)

    def on_action_refresh_activate(self, widget):
        """Reload the ARP cache list"""
        self.model.refresh()

    def on_treeview_hosts_row_activated(self, widget, path, column):
        """Treats the double click as the OK button was pressed"""
        self.ui.dialog.response(Gtk.ResponseType.OK)
