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

import gettext
import locale

from gwakeonlan.constants import APP_DOMAIN, DIR_LOCALE
from gwakeonlan.localize import (store_message,
                                 strip_colon,
                                 strip_underline,
                                 text)


# Load domain for translation
for module in (gettext, locale):
    module.bindtextdomain(APP_DOMAIN, DIR_LOCALE)
    module.textdomain(APP_DOMAIN)

# Import some translated messages from GTK+ domain
for message in ('_Cancel', 'General', '_OK'):
    store_message(strip_colon(strip_underline(message)),
                  strip_colon(strip_underline(text(message=message,
                                                   gtk30=True))))

# Import some translated messages from GTK+ domain and context
for message in ('_Refresh', ):
    store_message(strip_colon(strip_underline(message)),
                  strip_colon(strip_underline(text(message=message,
                                                   gtk30=True,
                                                   context='Stock label'))))

# Import some variations
store_message('Destination host',
              strip_colon(strip_underline(text(message='_Destination host:',
                                               gtk30=False))))
store_message('MAC Address',
              strip_colon(strip_underline(text(message='MAC _Address:',
                                               gtk30=False))))
store_message('Machine name',
              strip_colon(strip_underline(text(message='_Machine name:',
                                               gtk30=False))))
store_message('Request type',
              strip_colon(strip_underline(text(message='Request type:',
                                               gtk30=False))))
store_message('Select all',
              strip_underline(text(message='Select _All',
                                   gtk30=True)))
store_message('UDP port number',
              strip_colon(strip_underline(text(message='_UDP port number:',
                                               gtk30=False))))
