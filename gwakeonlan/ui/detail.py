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

from gwakeonlan.constants import BROADCAST_ADDRESS
from gwakeonlan.functions import format_mac_address
from gwakeonlan.localize import _
from gwakeonlan.ui.base import UIBase

SECTION_WINDOW_NAME = 'detail'


class UIDetail(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='detail.ui')
        # Initialize members
        self.parent = parent
        self.settings = settings
        self.options = options
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
        # Load icon from file
        self.load_image_file(self.ui.image_computer)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.dialog,
                                              section=SECTION_WINDOW_NAME)

    def show(self):
        """Show the dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.dialog.hide)
        response = 0
        self.ui.label_error.set_property('visible', False)
        self.ui.dialog.set_title(_('Edit machine')
                                 if self.do_get_mac_address()
                                 else _('Add machine'))
        while not response:
            response = self.ui.dialog.run()
            if response == Gtk.ResponseType.OK:
                # Check values for valid response
                err_msg = ''
                mac = (self.do_get_mac_address()
                       .replace(':', '')
                       .replace('.', '')
                       .replace('-', ''))
                if not self.do_get_machine_name():
                    err_msg = _('Missing machine name')
                    self.ui.text_machine_name.grab_focus()
                elif not (len(mac) == 12 and
                          all(c in '1234567890ABCDEF' for c in mac.upper())):
                    err_msg = _('Invalid MAC address')
                    self.ui.text_mac_address.grab_focus()
                elif (self.ui.radio_request_internet.get_active() and
                      self.do_get_destination() in ('', BROADCAST_ADDRESS)):
                    err_msg = _('Invalid destination host')
                    self.ui.text_destination_host.grab_focus()
                # There was an error, don't close the dialog
                if err_msg:
                    self.ui.label_error.set_property('visible', True)
                    self.ui.label_error.set_markup(
                        f'<span foreground="red"><b>{err_msg}</b></span>')
                    # Don't close the dialog if there's some error
                    response = 0
        self.ui.dialog.hide()
        return response

    def destroy(self):
        """Destroy the dialog"""
        logging.debug(f'{self.__class__.__name__} destroy')
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def do_get_destination(self):
        """Return the destination host"""
        return self.ui.text_destination_host.get_text()

    def do_get_mac_address(self):
        """Return the MAC address"""
        return format_mac_address(self.ui.text_mac_address.get_text())

    def do_get_machine_name(self):
        """Return the machine name"""
        return self.ui.text_machine_name.get_text()

    def do_get_port_number(self):
        """Return the port number"""
        return self.ui.spin_port_number.get_value_as_int()

    def do_get_request_type_internet(self):
        """Return if the request type is Internet"""
        return self.ui.radio_request_internet.get_active()

    def do_load_data(self, machine_name, mac_address, portnr, destination):
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

    def on_radio_request_type_toggled(self, widget):
        """A Radio button was pressed"""
        request_type_internet = self.ui.radio_request_internet.get_active()
        # Check the request type
        if request_type_internet:
            # If there was the broadcast address it will be deleted
            if self.do_get_destination() == BROADCAST_ADDRESS:
                self.ui.text_destination_host.set_text('')
        else:
            # For local request type the broadcast address will be used
            self.ui.text_destination_host.set_text(BROADCAST_ADDRESS)
        # Enable the destination fields accordingly to the request type
        self.ui.label_destination_host.set_sensitive(request_type_internet)
        self.ui.text_destination_host.set_sensitive(request_type_internet)
        # Hide previous errors
        self.ui.label_error.set_visible(False)
