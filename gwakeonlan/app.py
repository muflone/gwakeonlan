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

from gi.repository import Gio
from gi.repository import Gtk

from gwakeonlan.constants import APP_ID
from gwakeonlan.functions import get_ui_file
from gwakeonlan.gtkbuilder_loader import GtkBuilderLoader

from gwakeonlan.ui.main import MainWindow


class Application(Gtk.Application):
    def __init__(self, options):
        """Prepare the GtkApplication"""
        super(self.__class__, self).__init__(application_id=APP_ID)
        self.options = options
        self.connect("activate", self.activate)
        self.connect('startup', self.startup)

    def startup(self, application):
        """Configure the application during the startup"""
        self.ui = MainWindow(self, self.options)
        # Add the actions related to the app menu
        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.on_app_about_activate)
        self.add_action(action)
        # Add the shortcut action to the app menu
        # only for GTK+ 3.20.0 and higher
        if not Gtk.check_version(3, 20, 0):
            action = Gio.SimpleAction(name="shortcuts")
            action.connect("activate", self.on_app_shortcuts_activate)
            self.add_action(action)
        # Add the quit action to the app menu
        action = Gio.SimpleAction(name="quit")
        action.connect("activate", self.on_app_quit_activate)
        self.add_action(action)
        # Add the app menu
        builder_appmenu = GtkBuilderLoader(get_ui_file('appmenu.ui'))
        self.set_app_menu(builder_appmenu.app_menu)

    def activate(self, application):
        """Execute the application"""
        self.ui.run()

    def on_app_about_activate(self, action, data):
        """Show the about dialog from the app menu"""
        self.ui.on_button_about_clicked(self)

    def on_app_shortcuts_activate(self, action, data):
        """Show the shortcuts dialog from the app menu"""
        self.ui.on_button_shortcuts_clicked(action)

    def on_app_quit_activate(self, action, data):
        """Quit the application from the app menu"""
        self.ui.on_window_delete_event(self, None)
