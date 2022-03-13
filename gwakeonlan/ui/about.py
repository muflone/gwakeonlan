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
from gi.repository.GdkPixbuf import Pixbuf

from gwakeonlan.constants import (APP_AUTHOR,
                                  APP_AUTHOR_EMAIL,
                                  APP_COPYRIGHT,
                                  APP_NAME,
                                  APP_URL,
                                  APP_VERSION,
                                  FILE_CONTRIBUTORS,
                                  FILE_ICON,
                                  FILE_LICENSE,
                                  FILE_RESOURCES,
                                  FILE_TRANSLATORS)
from gwakeonlan.functions import (_,
                                  get_ui_file,
                                  readlines)
from gwakeonlan.gtkbuilder_loader import GtkBuilderLoader


class UIAbout(object):
    def __init__(self, parent, settings, options):
        """Prepare the about dialog"""
        self.settings = settings
        self.options = options
        # Retrieve the translators list
        translators = []
        for line in readlines(FILE_TRANSLATORS, False):
            if ':' in line:
                line = line.split(':', 1)[1]
            line = line.replace('(at)', '@').strip()
            if line not in translators:
                translators.append(line)
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('about.ui'))
        # Set various properties
        self.ui.dialog.set_program_name(APP_NAME)
        self.ui.dialog.set_version(_('Version {VERSION}').format(
            VERSION=APP_VERSION))
        self.ui.dialog.set_comments(
            _('Wake up your machines using Wake on LAN.'))
        self.ui.dialog.set_website(APP_URL)
        self.ui.dialog.set_copyright(APP_COPYRIGHT)
        # Prepare lists for authors and contributors
        authors = ['%s <%s>' % (APP_AUTHOR, APP_AUTHOR_EMAIL)]
        contributors = []
        for line in readlines(FILE_CONTRIBUTORS, False):
            contributors.append(line)
        if len(contributors) > 0:
            contributors.insert(0, _('Contributors:'))
            authors.extend(contributors)
        self.ui.dialog.set_authors(authors)
        self.ui.dialog.set_license(
            '\n'.join(readlines(FILE_LICENSE, True)))
        self.ui.dialog.set_translator_credits('\n'.join(translators))
        # Retrieve the external resources links
        # only for GTK+ 3.6.0 and higher
        if not Gtk.check_version(3, 6, 0):
            for line in readlines(FILE_RESOURCES, False):
                resource_type, resource_url = line.split(':', 1)
                self.ui.dialog.add_credit_section(
                    resource_type, (resource_url,))
        icon_logo = Pixbuf.new_from_file(str(FILE_ICON))
        self.ui.dialog.set_logo(icon_logo)
        self.ui.dialog.set_transient_for(parent)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def show(self):
        """Show the About dialog"""
        if self.options.autotest:
            GLib.timeout_add(500, self.ui.dialog.hide)
        self.ui.dialog.run()
        self.ui.dialog.hide()

    def destroy(self):
        """Destroy the About dialog"""
        self.ui.dialog.destroy()
        self.ui.dialog = None
