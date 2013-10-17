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

import struct
import socket
from gi.repository import Gtk

def formatMAC(mac):
  "Return the mac address formatted with colon"
  mac = mac.replace(':', '').replace('.', '')
  return ':'.join([mac[i:i+2] for i in xrange(0, len(mac), 2)]).upper()

def show_message_dialog_yesno(winParent, message, title, default_response):
  dialog = Gtk.MessageDialog(
    parent=winParent,
    flags=Gtk.DialogFlags.MODAL,
    type=Gtk.MessageType.QUESTION,
    buttons=Gtk.ButtonsType.YES_NO,
    message_format=message
  )
  dialog.set_title(title)
  if default_response:
    dialog.set_default_response(default_response)
  response = dialog.run()
  dialog.destroy()
  return response

def wake_on_lan(mac_address, portnr, destination):
  "Turn on remote machine using Wake On LAN."
  # Magic packet (6 times FF + 16 times MAC address)
  packet = 'FF' * 6 + mac_address.replace(':', '') * 16
  data = []
  for i in xrange(0, len(packet), 2):
    data.append(struct.pack('B', int(packet[i:i+2], 16)))

  # Send magic packet to the destination
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  if destination == '255.255.255.255':
    destination = '<broadcast>'
  sock.sendto(''.join(data), (destination, portnr))

_ = lambda x: x

__all__ = [
  'formatMAC',
  'show_message_dialog_yesno',
  'wake_on_lan',
  '_'
]
