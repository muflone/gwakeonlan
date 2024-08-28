##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2024 Fabio Castelli
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

from gi.repository import Gtk

from gwakeonlan.constants import APP_ID
from gwakeonlan.ui.main import UIMain


class Application(Gtk.Application):
    def __init__(self, options):
        """Prepare the GtkApplication"""
        super(self.__class__, self).__init__(application_id=APP_ID)
        self.options = options
        self.ui = None
        self.connect('activate', self.activate)
        self.connect('startup', self.startup)

    # noinspection PyUnusedLocal
    def startup(self, application):
        """Configure the application during the startup"""
        self.ui = UIMain(application=self,
                         options=self.options)

    # noinspection PyMethodOverriding
    def activate(self, application):
        """Execute the application"""
        self.ui.run()
