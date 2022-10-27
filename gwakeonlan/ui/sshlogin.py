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

from gwakeonlan.localize import _
from gwakeonlan.ui.base import UIBase
from gwakeonlan.mikrotik import Mikrotik

SECTION_WINDOW_NAME = 'sshlogin'


class UISSHLogin(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='ssh-login.ui')
        # Initialize members
        self.parent = parent
        self.settings = settings
        self.options = options
        # Mikrotik setup
        self.mikrotik = Mikrotik()
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
        self.ui.SSHLogin.set_transient_for(self.parent)
        # Load icon from file
        self.load_image_file(self.ui.image_computer)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.SSHLogin,
                                              section=SECTION_WINDOW_NAME)

    def show(self):
        """Show the dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.SSHLogin.hide)
        self.ui.label_error.set_property('visible', False)
        self.ui.SSHLogin.set_title(_('Input your router\'s credentials'))
        self.ui.SSHLogin.show_all()
        response = self.ui.SSHLogin.run()
        self.ui.SSHLogin.hide()
        return response

    def destroy(self):
        """Destroy the dialog"""
        logging.debug(f'{self.__class__.__name__} destroy')
        self.ui.SSHLogin.destroy()
        self.ui.SSHLogin = None

    def do_load_data(self, machine_name, mac_address, username, router, interface):
        """Load the fields with the specified values"""
        self.ui.text_username.set_text(username or "")
        self.ui.label_machine_name.set_label(machine_name or "")
        self.ui.label_mac_address.set_label(mac_address or "")
        self.ui.label_interface.set_label(interface or "")
        self.ui.label_mikrotik_router.set_label(router or "")
        self.ui.text_password.grab_focus()

    def set_error(self, msg):
        """Set the error message of the first try"""
        if msg != "":
            self.ui.label_error.set_property('visible', True)
            self.ui.label_error.set_label(f'<span foreground="red">{msg}</span>')
        else:
            self.ui.label_error.set_property('visible', False)

    def send_or_show(self):
        """Try sending the request, if not possible to login, then show the dialog and ask for credentials"""
        mac_address = self.ui.label_mac_address.get_label()
        username = self.ui.text_username.get_text()
        password = self.ui.text_password.get_text()
        router = self.ui.label_mikrotik_router.get_label()
        interface = self.ui.label_interface.get_label()
        self.set_error("")
        sent = self.mikrotik.wol(mac_address, username, router, interface, password)
        if sent is not True:
            self.set_error(sent)
            if self.show() == Gtk.ResponseType.APPLY:
                self.send_or_show()

