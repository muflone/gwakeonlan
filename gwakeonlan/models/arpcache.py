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

import logging
import os.path
import socket

from gwakeonlan.constants import FILE_ARP_CACHE
from gwakeonlan.models.abstract import ModelAbstract
from gwakeonlan.models.arpcache_item import ArpCacheItem


class ModelArpCache(ModelAbstract):
    COL_IPADDRESS = 0
    COL_MACADDRESS = 1
    COL_HOSTNAME = 2

    def add_data(self, item):
        """Add a new row to the model if it doesn't exist"""
        super(self.__class__, self).add_data(item)
        if item.ip_address not in self.rows:
            new_row = self.model.append((
                item.ip_address,
                item.mac_address.upper(),
                item.hostname
            ))
            self.rows[item.ip_address] = new_row

    def refresh(self):
        """Clear the model and reload all the hosts from the ARP cache file"""
        self.clear()
        # Read ARP cache file
        if os.path.isfile(FILE_ARP_CACHE):
            try:
                arpf = open(FILE_ARP_CACHE, 'r')
                # Skip first and last line
                for line in arpf.readlines()[1:]:
                    if line:
                        # Add IP Address and MAC address to the model
                        logging.debug(f'arp line:\n{line}')
                        arp_ip = line[:17].rstrip()
                        arp_mac = line[41:58].upper()
                        # Skip incomplete MAC addresses
                        if arp_mac != '00:00:00:00:00:00':
                            detected_hostname = socket.getfqdn(arp_ip)
                            # I will not trust of getfqdn if the returned
                            # hostname is the same of the source IP address
                            if detected_hostname == arp_ip:
                                detected_hostname = ''
                            logging.info(f'discovered {arp_ip} '
                                         f'with address {arp_mac}')
                            self.add_data(ArpCacheItem(
                                ip_address=arp_ip,
                                mac_address=arp_mac,
                                hostname=detected_hostname
                            ))
                arpf.close()
            except (FileNotFoundError, PermissionError):
                logging.error(f'unable to read {FILE_ARP_CACHE}')

    def get_ip_address(self, treeiter):
        """Returns the IP address for the selected TreeIter"""
        return self.model[treeiter][self.COL_IPADDRESS]

    def get_mac_address(self, treeiter):
        """Returns the MAC address for the selected TreeIter"""
        return self.model[treeiter][self.COL_MACADDRESS]

    def get_hostname(self, treeiter):
        """Returns the hostname for the selected TreeIter"""
        return self.model[treeiter][self.COL_HOSTNAME]
