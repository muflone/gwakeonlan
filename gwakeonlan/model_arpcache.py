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

import os.path
import socket
from gwakeonlan.constants import *


class ModelARPCache(object):
    COL_IPADDRESS = 0
    COL_MACADDRESS = 1
    COL_HOSTNAME = 2

    def __init__(self, model, settings):
        self.model = model
        self.settings = settings

    def clear(self):
        "Clear the model"
        return self.model.clear()

    def refresh(self):
        "Clear the model and reload all the hosts from the ARP cache file"
        self.clear()
        # Read ARP cache file
        if os.path.isfile(FILE_ARP_CACHE):
            try:
                arpf = open(FILE_ARP_CACHE, 'r')
                # Skip first and last line
                for line in arpf.readlines()[1:]:
                    if line:
                        # Add IP Address and MAC address to the model
                        self.settings.logText('arp line:\n%s' % line,
                                              VERBOSE_LEVEL_MAX)
                        arp_ip = line[:17].rstrip()
                        arp_mac = line[41:58].upper()
                        # Skip incomplete MAC addresses
                        if arp_mac != '00:00:00:00:00:00':
                            detected_hostname = socket.getfqdn(arp_ip)
                            # I will not trust of getfqdn if the returned
                            # hostname is the same of the source IP address
                            if detected_hostname == arp_ip:
                                detected_hostname = ''
                            self.settings.logText(
                                'discovered %s with address %s' % (
                                    arp_ip, arp_mac))
                            self.model.append(
                                [arp_ip, arp_mac, detected_hostname])
                arpf.close()
            except:
                self.settings.logText('unable to read %s' % FILE_ARP_CACHE)

    def get_ip_address(self, treeiter):
        "Returns the IP address for the selected TreeIter"
        return self.model[treeiter][self.__class__.COL_IPADDRESS]

    def get_mac_address(self, treeiter):
        "Returns the MAC address for the selected TreeIter"
        return self.model[treeiter][self.__class__.COL_MACADDRESS]

    def get_hostname(self, treeiter):
        "Returns the hostname for the selected TreeIter"
        return self.model[treeiter][self.__class__.COL_HOSTNAME]
