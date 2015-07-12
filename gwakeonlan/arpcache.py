##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2015 Fabio Castelli
#     License: GPL-2+
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
from gwakeonlan.model_arpcache import ModelARPCache
from gwakeonlan.constants import *
from gwakeonlan.functions import *


class ARPCacheWindow(object):
    def __init__(self, settings, winParent, show=False):
        """Prepare the ARP Cache dialog and optionally show it immediately"""
        # Load interface UI
        builder = Gtk.Builder()
        builder.add_from_file(FILE_UI_ARPCACHE)
        # Obtain widget references
        self.dialog = builder.get_object('dlgARPCache')
        self.tvwHosts = builder.get_object('tvwHosts')
        self.btnOK = builder.get_object('btnOK')
        self.btnCancel = builder.get_object('btnCancel')
        self.model = ModelARPCache(
            builder.get_object('modelARPCache'), settings)
        self.model.refresh()
        self.dialog.set_title(_('Pick a host from the ARP cache'))
        self.dialog.set_icon_from_file(FILE_ICON)
        self.dialog.set_transient_for(winParent)
        self.btnOK.set_label(gtk30_('_OK'))
        self.btnCancel.set_label(gtk30_('_Cancel'))
        # Connect signals from the glade file to the functions
        # with the same name
        builder.connect_signals(self)
        # Optionally show the dialog
        if show:
            self.show()

    def destroy(self):
        """Hide and destroy the ARP cache picker dialog"""
        self.dialog.destroy()
        self.dialog = None

    def show(self):
        """Show the ARP Cache picker dialog"""
        response = self.dialog.run()
        self.dialog.hide()
        return response

    def on_btnRefresh_clicked(self, widget):
        """Reload the ARP cache list"""
        self.model.refresh()

    def on_tvwHosts_row_activated(self, widget, path, column):
        """Treats the double click as the OK button was pressed"""
        self.dialog.response(Gtk.ResponseType.OK)

    def get_ip_address(self):
        """Returns the IP address of the selected row"""
        (model, treeiter) = self.tvwHosts.get_selection().get_selected()
        if treeiter:
            return self.model.get_ip_address(treeiter)

    def get_hostname(self):
        """Returns the hostname of the selected row"""
        (model, treeiter) = self.tvwHosts.get_selection().get_selected()
        if treeiter:
            return self.model.get_hostname(treeiter)

    def get_mac_address(self):
        """Returns the MAC address of the selected row"""
        (model, treeiter) = self.tvwHosts.get_selection().get_selected()
        if treeiter:
            return self.model.get_mac_address(treeiter)
