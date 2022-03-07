#!/usr/bin/env python3
##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2022 Fabio Castelli
#     License: GPL-3+
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

import gettext
import locale

import gi
gi.require_version('Gtk', '3.0')

from gwakeonlan.app import Application                             # noqa: E402
from gwakeonlan.constants import DIR_LOCALE, DOMAIN_NAME           # noqa: E402
from gwakeonlan.settings import Settings                           # noqa: E402


if __name__ == '__main__':
    # Load domain for translation
    for module in (gettext, locale):
        module.bindtextdomain(DOMAIN_NAME, DIR_LOCALE)
        module.textdomain(DOMAIN_NAME)

    # Load the settings from the configuration file
    settings = Settings()
    settings.load()

    # Start the application
    app = Application(settings)
    app.run(None)
