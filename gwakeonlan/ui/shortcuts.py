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

from gi.repository import Gtk

from gwakeonlan.localize import text, text_gtk30
from gwakeonlan.ui.base import UIBase


class UIShortcuts(UIBase):
    def __init__(self, parent):
        """Prepare the shortcuts dialog"""
        super().__init__(filename='shortcuts.ui')
        self.ui.shortcuts.set_transient_for(parent)
        # Initialize translations
        self.ui.shortcut_select_all.props.title = (
            text_gtk30('Select _All').replace('_', ''))
        # Initialize groups
        for widget in self.ui.get_objects_by_type(Gtk.ShortcutsGroup):
            widget.props.title = text(widget.props.title)
        # Initialize shortcuts
        for widget in self.ui.get_objects_by_type(Gtk.ShortcutsShortcut):
            widget.props.title = text(widget.props.title)

    def show(self):
        """Show the shortcuts dialog"""
        self.ui.shortcuts.show()

    def destroy(self):
        """Destroy the shortcuts dialog"""
        self.ui.shortcuts.destroy()
        self.ui.shortcuts = None
