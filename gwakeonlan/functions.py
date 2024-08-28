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

import itertools
import logging
import pathlib
import struct
import socket

from gi.repository import Gtk
from gi.repository import GdkPixbuf

from gwakeonlan.constants import DIR_UI


def format_mac_address(mac):
    """Return the mac address formatted with colon"""
    mac = mac.replace(':', '').replace('.', '').replace('-', '')
    return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)]).upper()


def get_pixbuf_from_icon_name(icon_name, size):
    """Get a Gdk.PixBuf from a theme icon"""
    theme = Gtk.IconTheme.get_default()
    path_icon_name = pathlib.Path(icon_name)
    if theme.has_icon(icon_name):
        # The icon was a theme icon
        icon = theme.load_icon(icon_name=icon_name,
                               size=size,
                               flags=Gtk.IconLookupFlags.USE_BUILTIN)
    elif theme.has_icon(path_icon_name.stem):
        # The theme contains an icon with the same file name
        icon = theme.load_icon(icon_name=path_icon_name.stem,
                               size=size,
                               flags=Gtk.IconLookupFlags.USE_BUILTIN)
    elif path_icon_name.is_file():
        # The icon was a full filename
        icon = GdkPixbuf.Pixbuf.new_from_file(icon_name)
    else:
        # The icon was not found in the current theme, search for filenames
        # with png or jpg extensions
        if path_icon_name.suffix.lower() in ('.png', '.jpg', '.xpm', '.svg'):
            filenames = (icon_name, )
        else:
            filenames = (f'{icon_name}.png',
                         f'{icon_name}.jpg',
                         f'{icon_name}.xpm',
                         f'{icon_name}.svg')
        # Search for filenames in icons and pixmaps directories
        icon = None
        search_in_paths = ('/usr/share/icons',
                           '/usr/share/pixmaps')
        for path, filename in itertools.product(search_in_paths, filenames):
            file_path = pathlib.Path(path) / filename
            if file_path.is_file():
                icon = GdkPixbuf.Pixbuf.new_from_file(str(file_path))
                break
    if icon:
        # If size is not correct then resize the icon to the requested size
        if icon.get_width() != size or icon.get_height() != size:
            icon = icon.scale_simple(size, size,
                                     GdkPixbuf.InterpType.BILINEAR)
    else:
        logging.warning(f'missing icon: {icon_name}')
    return icon


def get_treeview_selected_row(widget):
    """Return the selected row in a GtkTreeView"""
    return widget.get_selection().get_selected()[1]


def get_ui_file(filename):
    """Return the full path of a Glade/UI file"""
    return str(DIR_UI / filename)


def process_events():
    """Process every pending GTK+ event"""
    while Gtk.events_pending():
        Gtk.main_iteration()


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


def show_message_dialog_yesno(parent, message, title, default_response):
    """Show a GtkMessageDialog with yes and no buttons"""
    dialog = Gtk.MessageDialog(
        parent=parent,
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


def wake_on_lan(mac_address, port_number, destination):
    """Turn on remote machine using Wake On LAN"""
    logging.info(f'turning on: {mac_address} '
                 f'through {destination} '
                 f'using port number {port_number}')
    # Magic packet (6 times FF + 16 times MAC address)
    packet = 'FF' * 6 + mac_address.replace(':', '') * 16
    data = []
    for i in range(0, len(packet), 2):
        data.append(struct.pack('B', int(packet[i:i+2], 16)))

    # Send magic packet to the destination
    logging.info(f'sending packet {packet} [{len(packet)}/{len(data)}]\n')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if destination == '255.255.255.255':
        destination = '<broadcast>'
    data = b''.join(data)
    for _ in range(10):
        sock.sendto(data, (destination, port_number))
