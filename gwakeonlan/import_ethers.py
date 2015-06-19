# @license AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.html>
# @author Copyright (C) 2015 Robin Schneider <ypid@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, version 3 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

from gwakeonlan.constants import DEFAULT_UDP_PORT, BROADCAST_ADDRESS


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
