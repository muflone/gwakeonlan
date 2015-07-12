##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2015 Fabio Castelli
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

import os
import os.path
import optparse
import time
import ConfigParser
from gwakeonlan.functions import *
from gwakeonlan.constants import *

SECTION_MAINWIN = 'main window'
SECTION_HOSTS = 'hosts'

class Settings(object):
  def __init__(self):
    self.settings = {}
    self.model = None

    # Command line options and arguments
    parser = optparse.OptionParser(usage='usage: %prog [options]')
    parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL)
    parser.add_option('-v', '--verbose', dest='verbose_level',
                      action='store_const', const=VERBOSE_LEVEL_MAX,
                      help='show error and information messages')
    parser.add_option('-q', '--quiet', dest='verbose_level',
                      action='store_const', const=VERBOSE_LEVEL_QUIET,
                      help='hide error and information messages')
    (self.options, self.arguments) = parser.parse_args()
    # Parse settings from the configuration file
    self.config = ConfigParser.RawConfigParser()
    # Allow saving in case sensitive (useful for machine names)
    self.config.optionxform = str
    # Determine which filename to use for settings
    self.filename = os.path.exists(FILE_SETTINGS_OLD) and FILE_SETTINGS_OLD or FILE_SETTINGS_NEW
    if self.filename:
      self.logText('Loading settings from %s' % self.filename, VERBOSE_LEVEL_MAX)
      self.config.read(self.filename)

  def load(self):
    "Load window settings"
    if self.config.has_section(SECTION_MAINWIN):
      self.logText('Retrieving window settings', VERBOSE_LEVEL_MAX)
      # Retrieve window position and size
      if self.config.has_option(SECTION_MAINWIN, 'left'):
        self.settings['left'] = self.config.getint(SECTION_MAINWIN, 'left')
      if self.config.has_option(SECTION_MAINWIN, 'top'):
        self.settings['top'] = self.config.getint(SECTION_MAINWIN, 'top')
      if self.config.has_option(SECTION_MAINWIN, 'width'):
        self.settings['width'] = self.config.getint(SECTION_MAINWIN, 'width')
      if self.config.has_option(SECTION_MAINWIN, 'height'):
        self.settings['height'] = self.config.getint(SECTION_MAINWIN, 'height')

  def load_hosts(self, model):
    "Load hosts settings"
    self.model = model
    if self.config.has_section(SECTION_HOSTS):
      for machine in self.config.items(SECTION_HOSTS):
        self.logText('Loading machine: %s' % machine[0], VERBOSE_LEVEL_MAX)
        machine = ('%s\\%s\\255.255.255.255\\9' % machine).split('\\', 4)
        self.model.add_machine(False, machine[0],
          formatMAC(machine[1]), int(machine[3]), machine[2])

  def get_value(self, name, default=None):
    return self.settings.get(name, default)

  def set_sizes(self, winParent):
    "Save configuration for main window"
    # Main window settings section
    self.logText('Saving window settings', VERBOSE_LEVEL_MAX)
    if not self.config.has_section(SECTION_MAINWIN):
      self.config.add_section(SECTION_MAINWIN)
    # Window position
    position = winParent.get_position()
    self.config.set(SECTION_MAINWIN, 'left', position[0])
    self.config.set(SECTION_MAINWIN, 'top', position[1])
    # Window size
    size = winParent.get_size()
    self.config.set(SECTION_MAINWIN, 'width', size[0])
    self.config.set(SECTION_MAINWIN, 'height', size[1])

  def save(self):
    "Save the whole configuration"
    # Hosts section
    if self.config.has_section(SECTION_HOSTS):
      self.config.remove_section(SECTION_HOSTS)
    self.config.add_section(SECTION_HOSTS)
    for machine in self.model:
      self.logText('Saving machine: %s' % self.model.get_machine_name(machine), 
      VERBOSE_LEVEL_MAX)
      self.config.set(SECTION_HOSTS,
        self.model.get_machine_name(machine), '%s\\%s\\%d' % (
        self.model.get_mac_address(machine),
        self.model.get_destination(machine),
        self.model.get_portnr(machine))
      )
    # Always save the settings in the new configuration file
    file_settings = open(FILE_SETTINGS_NEW, mode='w')
    self.logText('Saving settings to %s' % FILE_SETTINGS_NEW, VERBOSE_LEVEL_MAX)
    self.config.write(file_settings)
    file_settings.close()
    # If the read configuration at starup is the old configuration file
    # the old configuration file will be deleted and the new file will be used
    if self.filename == FILE_SETTINGS_OLD:
      self.logText('Removing old settings from %s' % FILE_SETTINGS_OLD, VERBOSE_LEVEL_MAX)
      os.remove(FILE_SETTINGS_OLD)
      self.filename = FILE_SETTINGS_NEW

  def logText(self, text, verbose_level=VERBOSE_LEVEL_NORMAL):
    "Print a text with current date and time based on verbose level"
    if verbose_level <= self.options.verbose_level:
      print '[%s] %s' % (time.strftime('%Y/%m/%d %H:%M:%S'), text)
