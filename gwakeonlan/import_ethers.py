##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Robin Schneider <ypid@riseup.net>
#   Copyright: 2015 Robin Schneider <ypid@riseup.net>
#     License: GPL-3+
#
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

import re

from gwakeonlan.constants import BROADCAST_ADDRESS, DEFAULT_UDP_PORT


class ImportEthers(object):

    def __init__(self, import_l3_dest=BROADCAST_ADDRESS):
        self.import_l3_dest = import_l3_dest

    def import_file(self, filepath, add_function):
        with open(filepath, 'r') as import_fh:
            for line in import_fh:
                if re.match(r'(?:#|\s*$)', line):
                    continue
                mac_address, machine_name = line.split()

                add_function(
                    False,
                    machine_name,
                    mac_address,
                    DEFAULT_UDP_PORT,
                    self.import_l3_dest,
                )
