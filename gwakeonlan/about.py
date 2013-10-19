##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <webreg@vbsimple.net>
#   Copyright: 2009-2013 Fabio Castelli
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
from gi.repository.GdkPixbuf import Pixbuf
from gwakeonlan.constants import *

class AboutWindow(object):
  def __init__(self, winParent, show = False):
    builder = Gtk.Builder()
    builder.add_from_file(FILE_UI_ABOUT)
    # Obtain widget references
    self.dialog = builder.get_object("dialogAbout")
    # Set various properties
    self.dialog.set_program_name(APP_NAME)
    self.dialog.set_version('Version %s' % APP_VERSION)
    self.dialog.set_comments(APP_DESCRIPTION)
    self.dialog.set_website(APP_URL)
    self.dialog.set_copyright(APP_COPYRIGHT)
    self.dialog.set_authors(['%s <%s>' % (APP_AUTHOR, APP_AUTHOR_EMAIL)])
    icon_logo = Pixbuf.new_from_file(FILE_ICON)
    self.dialog.set_logo(icon_logo)
    self.dialog.set_transient_for(winParent)
    # Optionally show the dialog
    if show:
      self.show()

  def show(self):
    "Show the About dialog"
    self.dialog.run()
    self.dialog.hide()

  def destroy(self):
    "Destroy the About dialog"
    self.dialog.destroy()
    self.dialog = None
