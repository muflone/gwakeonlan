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

from gi.repository import GLib
from gi.repository import Gtk

from gwakeonlan.constants import FILE_ICON
from gwakeonlan.functions import get_treeview_selected_row
from gwakeonlan.localize import _, text_gtk30
from gwakeonlan.models.arpcache import ModelArpCache
from gwakeonlan.ui.base import UIBase


class UIArpCache(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the ARP Cache dialog"""
        super().__init__(filename='arpcache.ui')
        self.settings = settings
        self.options = options
        self.model = ModelArpCache(self.ui.model)
        self.model.refresh()
        self.ui.dialog.set_title(_('Pick a host from the ARP cache'))
        self.ui.dialog.set_icon_from_file(str(FILE_ICON))
        self.ui.dialog.set_transient_for(parent)
        self.ui.button_ok.set_label(text_gtk30('_OK'))
        self.ui.button_cancel.set_label(text_gtk30('_Cancel'))
        self.ui.button_refresh.set_label(text_gtk30('_Refresh', 'Stock label'))
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def destroy(self):
        """Hide and destroy the ARP cache picker dialog"""
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def show(self):
        """Show the ARP Cache picker dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.dialog.hide)
        response = self.ui.dialog.run()
        self.ui.dialog.hide()
        return response

    def on_button_refresh_clicked(self, widget):
        """Reload the ARP cache list"""
        self.model.refresh()

    def on_treeview_hosts_row_activated(self, widget, path, column):
        """Treats the double click as the OK button was pressed"""
        self.ui.dialog.response(Gtk.ResponseType.OK)

    def get_ip_address(self):
        """Returns the IP address of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_ip_address(treeiter)

    def get_hostname(self):
        """Returns the hostname of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_hostname(treeiter)

    def get_mac_address(self):
        """Returns the MAC address of the selected row"""
        treeiter = get_treeview_selected_row(self.ui.treeview_hosts)
        if treeiter:
            return self.model.get_mac_address(treeiter)
