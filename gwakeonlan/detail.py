##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2020 Fabio Castelli
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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

from gwakeonlan.constants import *
from gwakeonlan.functions import *


class DetailWindow(object):
    def __init__(self, winParent, settings, show=False):
        self.settings = settings
        """Prepare the detail dialog and optionally show it immediately"""
        # Load interface UI
        builder = Gtk.Builder()
        builder.add_from_file(FILE_UI_DETAIL)
        # Obtain widget references
        self.dialog = builder.get_object('dlgDetail')
        self.cboMachineName = builder.get_object('cboMachineName')
        self.txtMachineName = builder.get_object('txtMachineName')
        self.txtMACAddress = builder.get_object('txtMACAddress')
        self.spinPortNumber = builder.get_object('spinPortNumber')
        self.radioRequestLocal = builder.get_object('radioRequestLocal')
        self.radioRequestInternet = builder.get_object('radioRequestInternet')
        self.lblDestinationHost = builder.get_object('lblDestinationHost')
        self.txtDestinationHost = builder.get_object('txtDestinationHost')
        self.btnOK = builder.get_object('btnOK')
        self.btnCancel = builder.get_object('btnCancel')
        self.lblError = builder.get_object('lblError')
        # Set various properties
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
        """Hide and destroy the Add/Delete machine dialog"""
        self.dialog.destroy()
        self.dialog = None

    def show(self):
        """Show the Add/Edit machine dialog"""
        if self.settings.options.autotest:
            GLib.timeout_add(500, self.dialog.hide)
        response = 0
        self.lblError.set_property('visible', False)
        self.dialog.set_title(self.get_mac_address() and _('Edit machine') or
                              _('Add machine'))
        while not response:
            response = self.dialog.run()
            if response == Gtk.ResponseType.OK:
                # Check values for valid response
                err_msg = ''
                mac = self.get_mac_address().replace(':', '').replace('.', '')
                if not self.get_machine_name():
                    err_msg = _('Missing machine name')
                    self.txtMachineName.grab_focus()
                elif not (len(mac) == 12 and
                          all(c in '1234567890ABCDEF' for c in mac.upper())):
                    err_msg = _('Invalid MAC address')
                    self.txtMACAddress.grab_focus()
                elif self.radioRequestInternet.get_active() and \
                        self.get_destination() in ('', BROADCAST_ADDRESS):
                    err_msg = _('Invalid destination host')
                    self.txtDestinationHost.grab_focus()
                # There was an error, don't close the dialog
                if err_msg:
                    self.lblError.set_property('visible', True)
                    self.lblError.set_markup(
                        '<span foreground="red"><b>%s</b></span>' % err_msg)
                    # Don't close the dialog if there's some error
                    response = 0
        self.dialog.hide()
        return response

    def get_machine_name(self):
        """Return the machine name"""
        return self.txtMachineName.get_text()

    def get_mac_address(self):
        """Return the MAC address"""
        return formatMAC(self.txtMACAddress.get_text())

    def get_portnr(self):
        """Return the port number"""
        return self.spinPortNumber.get_value_as_int()

    def get_destination(self):
        """Return the destination host"""
        return self.txtDestinationHost.get_text()

    def get_request_type_internet(self):
        """Return if the request type is Internet"""
        return self.radioRequestInternet.get_active()

    def on_radioRequestType_toggled(self, widget):
        """A Radio button was pressed"""
        request_type_internet = self.radioRequestInternet.get_active()
        # Check the request type
        if request_type_internet:
            # If there was the broadcast address it will be deleted
            if self.get_destination() == BROADCAST_ADDRESS:
                self.txtDestinationHost.set_text('')
        else:
            # For local request type the broadcast address will be used
            self.txtDestinationHost.set_text(BROADCAST_ADDRESS)
        # Enable the destination fields accordingly to the request type
        self.lblDestinationHost.set_sensitive(request_type_internet)
        self.txtDestinationHost.set_sensitive(request_type_internet)
        # Hide previous errors
        self.lblError.set_visible(False)

    def load_data(self, machine_name, mac_address, portnr, destination):
        """Load the fields with the specified values"""
        self.txtMachineName.set_text(machine_name)
        self.txtMACAddress.set_text(mac_address)
        self.spinPortNumber.set_value(portnr)
        self.txtDestinationHost.set_text(destination)
        if destination in (BROADCAST_ADDRESS, ''):
            self.radioRequestLocal.set_active(True)
            self.txtDestinationHost.set_sensitive(False)
        else:
            self.radioRequestInternet.set_active(True)
            self.txtDestinationHost.set_sensitive(True)
        self.txtMachineName.grab_focus()
