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

from gettext import gettext, dgettext
import logging
import struct
import socket

from gi.repository import Gtk

from gwakeonlan.constants import DIR_UI

localized_messages = {}


def formatMAC(mac):
    """Return the mac address formatted with colon"""
    mac = mac.replace(':', '').replace('.', '')
    return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)]).upper()


def show_message_dialog_yesno(winParent, message, title, default_response):
    """Show a GtkMessageDialog with yes and no buttons"""
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


def wake_on_lan(mac_address, portnr, destination, settings):
    """Turn on remote machine using Wake On LAN."""
    logging.info('turning on: %s through %s using port number %d' % (
        mac_address, destination, portnr))
    # Magic packet (6 times FF + 16 times MAC address)
    packet = 'FF' * 6 + mac_address.replace(':', '') * 16
    data = []
    for i in range(0, len(packet), 2):
        data.append(struct.pack('B', int(packet[i:i+2], 16)))

    # Send magic packet to the destination
    logging.info('sending packet %s [%d/%d]\n' % (
        packet, len(packet), len(data)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if destination == '255.255.255.255':
        destination = '<broadcast>'
    data = b''.join(data)
    [sock.sendto(data, (destination, portnr)) for _ in range(0, 10)]


def readlines(filename, empty_lines=False):
    """Read all the lines of a filename, optionally skipping empty lines"""
    result = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line or empty_lines:
                result.append(line)
        f.close()
    return result


def process_events():
    """Process every pending GTK+ event"""
    while Gtk.events_pending():
        Gtk.main_iteration()


def text(message, gtk30=False, context=None):
    """Return a translated message and cache it for reuse"""
    if message not in localized_messages:
        if gtk30:
            # Get a message translated from GTK+ 3 domain
            full_message = message if not context else f'{context}\04{message}'
            localized_messages[message] = dgettext('gtk30', full_message)
            # Fix for untranslated messages with context
            if context and localized_messages[message] == full_message:
                localized_messages[message] = dgettext('gtk30', message)
        else:
            localized_messages[message] = gettext(message)
    return localized_messages[message]


def text_gtk30(message, context=None):
    """Return a translated text from GTK+ 3.0"""
    return text(message=message, gtk30=True, context=context)


def store_message(message, translated):
    """Store a translated message in the localized_messages list"""
    localized_messages[message] = translated


def get_ui_file(filename):
    """Return the full path of a Glade/UI file"""
    return str(DIR_UI / filename)


def get_treeview_selected_row(widget):
    """Return the selected row in a GtkTreeView"""
    return widget.get_selection().get_selected()[1]


# This special alias is used to track localization requests to catch
# by xgettext. The text() calls aren't tracked by xgettext
_ = text

__all__ = [
    'formatMAC',
    'show_message_dialog_yesno',
    'wake_on_lan',
    'readlines',
    'process_events',
    'text',
    'text_gtk30',
    'store_message',
    'get_ui_file',
    'localized_messages',
    'get_treeview_selected_row',
    '_',
]
