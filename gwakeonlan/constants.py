##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2020 Fabio Castelli
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

import sys
import os.path

import xdg.BaseDirectory


# Application constants
APP_NAME = 'gWakeOnLAN'
APP_VERSION = '0.7.1'
APP_DESCRIPTION = 'Wake up your machines using Wake on LAN.'
APP_ID = 'gwakeonlan.muflone.com'
APP_URL = 'https://www.muflone.com/gwakeonlan'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'muflone@muflone.com'
APP_COPYRIGHT = 'Copyright 2009-2020 %s' % APP_AUTHOR
# Other constants
DEFAULT_UDP_PORT = 9
BROADCAST_ADDRESS = '255.255.255.255'
DOMAIN_NAME = 'gwakeonlan'
VERBOSE_LEVEL_QUIET = 0
VERBOSE_LEVEL_NORMAL = 1
VERBOSE_LEVEL_MAX = 2

# Paths constants
# If there's a file data/gwakeonlan.png then the shared data are searched in
# relative paths, else the standard paths are used
if os.path.isfile(os.path.join('data', 'gwakeonlan.png')):
    DIR_PREFIX = '.'
    DIR_LOCALE = os.path.join(DIR_PREFIX, 'locale')
    DIR_DOCS = os.path.join(DIR_PREFIX, 'doc')
else:
    DIR_PREFIX = os.path.join(sys.prefix, 'share', 'gwakeonlan')
    DIR_LOCALE = os.path.join(sys.prefix, 'share', 'locale')
    DIR_DOCS = os.path.join(sys.prefix, 'share', 'doc', 'gwakeonlan')
# Set the paths for the folders
DIR_DATA = os.path.join(DIR_PREFIX, 'data')
DIR_UI = os.path.join(DIR_PREFIX, 'ui')
DIR_SETTINGS = xdg.BaseDirectory.save_config_path(DOMAIN_NAME)
# Set the paths for the UI files
FILE_UI_MAIN = os.path.join(DIR_UI, 'main.glade')
FILE_UI_DETAIL = os.path.join(DIR_UI, 'detail.glade')
FILE_UI_ARPCACHE = os.path.join(DIR_UI, 'arpcache.glade')
FILE_UI_ABOUT = os.path.join(DIR_UI, 'about.glade')
FILE_UI_APPMENU = os.path.join(DIR_UI, 'appmenu.ui')
# Set the paths for the data files
FILE_ICON = os.path.join(DIR_DATA, 'gwakeonlan.png')
FILE_CONTRIBUTORS = os.path.join(DIR_DOCS, 'contributors')
FILE_TRANSLATORS = os.path.join(DIR_DOCS, 'translators')
FILE_LICENSE = os.path.join(DIR_DOCS, 'license')
FILE_RESOURCES = os.path.join(DIR_DOCS, 'resources')
# Set the paths for configuration files
FILE_SETTINGS_OLD = os.path.expanduser('~/.gwakeonlan')
FILE_SETTINGS_NEW = os.path.join(DIR_SETTINGS, 'settings.conf')
# Set the paths for others files
FILE_ARP_CACHE = '/proc/net/arp'
