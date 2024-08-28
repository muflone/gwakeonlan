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

import configparser
import logging

from gwakeonlan.constants import BROADCAST_ADDRESS, DEFAULT_UDP_PORT
from gwakeonlan.functions import format_mac_address
from gwakeonlan.models.machine_item import MachineItem

POSITION_LEFT = 'left'
POSITION_TOP = 'top'
SIZE_WIDTH = 'width'
SIZE_HEIGHT = 'height'

DEFAULT_VALUES = {}

SECTION_HOSTS = 'hosts'


class Settings(object):
    def __init__(self, filename, case_sensitive):
        self.model = None
        # Parse settings from the configuration file
        self.config = configparser.RawConfigParser()
        # Set case sensitiveness if requested
        if case_sensitive:
            self.config.optionxform = str
        # Determine which filename to use for settings
        self.filename = filename
        logging.debug(f'Loading settings from {self.filename}')
        self.config.read(self.filename)

    def get(self, section, option, default=None):
        """Get an option from a specific section"""
        if (self.config.has_section(section) and
                self.config.has_option(section, option)):
            return self.config.get(section, option)
        else:
            return default

    def set(self, section, option, value):
        """Save an option in a specific section"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_boolean(self, section, option, default=None):
        """Get a boolean option from a specific section"""
        return self.get(section, option, default) == '1'

    def set_boolean(self, section, option, value):
        """Save a boolean option in a specific section"""
        self.set(section, option, '1' if value else '0')

    def get_int(self, section, option, default=0):
        """Get an integer option from a specific section"""
        return int(self.get(section, option, default))

    def set_int(self, section, option, value):
        """Set an integer option from a specific section"""
        self.set(section, option, int(value))

    def get_list(self, section, option, separator=','):
        """Get an option list from a specific section"""
        value = self.get(section, option, '')
        if len(value):
            return [v.strip() for v in value.split(separator)]

    def load_preferences(self):
        """Load preferences"""
        for option in DEFAULT_VALUES:
            self.set_preference(option, self.get_preference(option))

    def get_preference(self, option):
        """Get a preference value by option name"""
        section, default = DEFAULT_VALUES[option]
        if isinstance(default, bool):
            method_get = self.get_boolean
        elif isinstance(default, int):
            method_get = self.get_int
        else:
            method_get = self.get
        return method_get(section=section,
                          option=option,
                          default=default)

    def set_preference(self, option, value):
        """Set a preference value by option name"""
        section, default = DEFAULT_VALUES[option]
        if isinstance(default, bool):
            method_set = self.set_boolean
        elif isinstance(default, int):
            method_set = self.set_int
        else:
            method_set = self.set
        return method_set(section=section,
                          option=option,
                          value=value)

    def save(self):
        """Save the whole configuration"""
        file_settings = open(self.filename, mode='w')
        logging.debug(f'Saving settings to {self.filename}')
        self.config.write(file_settings)
        file_settings.close()

    def get_sections(self):
        """Return the list of the sections"""
        return self.config.sections()

    def get_options(self, section):
        """Return the list of the options in a section"""
        return self.config.options(section)

    def unset_option(self, section, option):
        """Remove an option from a section"""
        return self.config.remove_option(section, option)

    def clear(self):
        """Remove every data in the settings"""
        for section in self.get_sections():
            self.config.remove_section(section)

    def restore_window_position(self, window, section):
        """Restore the saved window size and position"""
        if (self.get_int(section, SIZE_WIDTH) and
                self.get_int(section, SIZE_HEIGHT)):
            window.set_default_size(
                self.get_int(section, SIZE_WIDTH, -1),
                self.get_int(section, SIZE_HEIGHT, -1))
        if (self.get_int(section, POSITION_LEFT) and
                self.get_int(section, POSITION_TOP)):
            window.move(
                self.get_int(section, POSITION_LEFT),
                self.get_int(section, POSITION_TOP))

    def save_window_position(self, window, section):
        """Save the window size and position"""
        position = window.get_position()
        self.set_int(section, POSITION_LEFT, position[0])
        self.set_int(section, POSITION_TOP, position[1])
        size = window.get_size()
        self.set_int(section, SIZE_WIDTH, size[0])
        self.set_int(section, SIZE_HEIGHT, size[1])

    def load_hosts(self, model, icon):
        """Load hosts settings"""
        self.model = model
        if self.config.has_section(SECTION_HOSTS):
            for machine in self.config.items(SECTION_HOSTS):
                logging.debug(f'Loading machine: {machine[0]}')
                # Fix machine configuration from older gWakeOnLAN versions
                machine = [machine[0], ] + machine[1].split('\\', 4)
                if len(machine) == 2:
                    machine.append(BROADCAST_ADDRESS)
                if len(machine) == 3:
                    machine.append(DEFAULT_UDP_PORT)
                # Add the machine to the model
                self.model.add_data(
                    MachineItem(name=machine[0],
                                mac_address=format_mac_address(machine[1]),
                                port_number=int(machine[3]),
                                destination=machine[2],
                                icon=icon))

    def save_hosts(self, model):
        """Save hosts settings"""
        if self.config.has_section(SECTION_HOSTS):
            self.config.remove_section(SECTION_HOSTS)
        self.config.add_section(SECTION_HOSTS)
        for machine in model:
            treeiter = self.model.get_iter(machine)
            logging.debug(
                f'Saving machine: {self.model.get_machine_name(treeiter)}')
            self.config.set(
                SECTION_HOSTS,
                self.model.get_machine_name(treeiter),
                f'{self.model.get_mac_address(treeiter)}\\'
                f'{self.model.get_destination(treeiter)}\\'
                f'{self.model.get_port_number(treeiter)}'
            )
