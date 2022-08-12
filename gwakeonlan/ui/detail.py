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

from gwakeonlan.constants import BROADCAST_ADDRESS, FILE_ICON
from gwakeonlan.functions import format_mac_address
from gwakeonlan.localize import _, text_gtk30
from gwakeonlan.ui.base import UIBase


class UIDetail(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the detail dialog"""
        super().__init__(filename='detail.ui')
        self.settings = settings
        self.options = options
        # Set various properties
        self.ui.dialog.set_icon_from_file(str(FILE_ICON))
        self.ui.dialog.set_transient_for(parent)
        self.ui.button_ok.set_label(text_gtk30('_OK'))
        self.ui.button_cancel.set_label(text_gtk30('_Cancel'))
        # Load icon from file
        self.load_image_file(self.ui.image_computer)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def destroy(self):
        """Hide and destroy the Add/Delete machine dialog"""
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def show(self):
        """Show the Add/Edit machine dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.dialog.hide)
        response = 0
        self.ui.label_error.set_property('visible', False)
        self.ui.dialog.set_title(_('Edit machine')
                                 if self.get_mac_address()
                                 else _('Add machine'))
        while not response:
            response = self.ui.dialog.run()
            if response == Gtk.ResponseType.OK:
                # Check values for valid response
                err_msg = ''
                mac = (self.get_mac_address()
                       .replace(':', '')
                       .replace('.', '')
                       .replace('-', ''))
                if not self.get_machine_name():
                    err_msg = _('Missing machine name')
                    self.ui.text_machine_name.grab_focus()
                elif not (len(mac) == 12 and
                          all(c in '1234567890ABCDEF' for c in mac.upper())):
                    err_msg = _('Invalid MAC address')
                    self.ui.text_mac_address.grab_focus()
                elif (self.ui.radio_request_internet.get_active() and
                      self.get_destination() in ('', BROADCAST_ADDRESS)):
                    err_msg = _('Invalid destination host')
                    self.ui.text_destination_host.grab_focus()
                # There was an error, don't close the dialog
                if err_msg:
                    self.ui.label_error.set_property('visible', True)
                    self.ui.label_error.set_markup(
                        '<span foreground="red"><b>%s</b></span>' % err_msg)
                    # Don't close the dialog if there's some error
                    response = 0
        self.ui.dialog.hide()
        return response

    def get_machine_name(self):
        """Return the machine name"""
        return self.ui.text_machine_name.get_text()

    def get_mac_address(self):
        """Return the MAC address"""
        return format_mac_address(self.ui.text_mac_address.get_text())

    def get_port_number(self):
        """Return the port number"""
        return self.ui.spin_port_number.get_value_as_int()

    def get_destination(self):
        """Return the destination host"""
        return self.ui.text_destination_host.get_text()

    def get_request_type_internet(self):
        """Return if the request type is Internet"""
        return self.ui.radio_request_internet.get_active()

    def on_radio_request_type_toggled(self, widget):
        """A Radio button was pressed"""
        request_type_internet = self.ui.radio_request_internet.get_active()
        # Check the request type
        if request_type_internet:
            # If there was the broadcast address it will be deleted
            if self.get_destination() == BROADCAST_ADDRESS:
                self.ui.text_destination_host.set_text('')
        else:
            # For local request type the broadcast address will be used
            self.ui.text_destination_host.set_text(BROADCAST_ADDRESS)
        # Enable the destination fields accordingly to the request type
        self.ui.label_destination_host.set_sensitive(request_type_internet)
        self.ui.text_destination_host.set_sensitive(request_type_internet)
        # Hide previous errors
        self.ui.label_error.set_visible(False)

    def load_data(self, machine_name, mac_address, portnr, destination):
        """Load the fields with the specified values"""
        self.ui.text_machine_name.set_text(machine_name)
        self.ui.text_mac_address.set_text(mac_address)
        self.ui.spin_port_number.set_value(portnr)
        self.ui.text_destination_host.set_text(destination)
        if destination in (BROADCAST_ADDRESS, ''):
            self.ui.radio_request_local.set_active(True)
            self.ui.text_destination_host.set_sensitive(False)
        else:
            self.ui.radio_request_internet.set_active(True)
            self.ui.text_destination_host.set_sensitive(True)
        self.ui.text_machine_name.grab_focus()
