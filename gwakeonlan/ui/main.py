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
import time

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from gi.repository import Gtk

from gwakeonlan.constants import (FILE_ICON,
                                  APP_NAME,
                                  BROADCAST_ADDRESS, DEFAULT_UDP_PORT,
                                  FILE_SETTINGS)
from gwakeonlan.functions import (format_mac_address,
                                  get_pixbuf_from_icon_name,
                                  get_treeview_selected_row,
                                  process_events,
                                  show_message_dialog_yesno,
                                  wake_on_lan)
from gwakeonlan.import_ethers import ImportEthers
from gwakeonlan.localize import _, text
from gwakeonlan.settings import Settings
from gwakeonlan.models.machine_item import MachineItem
from gwakeonlan.models.machines import ModelMachines
from gwakeonlan.ui.about import UIAbout
from gwakeonlan.ui.base import UIBase
from gwakeonlan.ui.arpcache import UIArpCache
from gwakeonlan.ui.detail import UIDetail
from gwakeonlan.ui.shortcuts import UIShortcuts

SECTION_WINDOW_NAME = 'main window'


class UIMain(UIBase):
    def __init__(self, application, options):
        """Prepare the main window"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='main.ui')
        # Initialize members
        self.application = application
        self.options = options
        self.detected_addresses = {}
        self.model_machines = None
        # Load icons
        self.icon_empty = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,
                                               True, 8, 24, 24)
        self.icon_empty.fill(0)
        self.icon_yes = get_pixbuf_from_icon_name('gtk-yes', 24)
        self.icon_no = get_pixbuf_from_icon_name('gtk-no', 24)
        # Load settings
        self.settings = Settings(filename=FILE_SETTINGS,
                                 case_sensitive=True)
        self.settings.load_preferences()
        self.settings_map = {}
        # Load UI
        self.load_ui()
        # Prepare the models
        self.model_machines = ModelMachines(self.ui.model)
        # Load the others dialogs
        self.detail = UIDetail(self.ui.window, self.settings, options)
        # Complete initialization
        self.startup()

    def load_ui(self):
        """Load the interface UI"""
        logging.debug(f'{self.__class__.__name__} load UI')
        # Initialize titles and tooltips
        self.set_titles()
        # Initialize Gtk.HeaderBar
        self.ui.header_bar.props.title = self.ui.window.get_title()
        self.ui.window.set_titlebar(self.ui.header_bar)
        self.set_buttons_icons(buttons=[self.ui.button_turnon,
                                        self.ui.button_add,
                                        self.ui.button_edit,
                                        self.ui.button_delete,
                                        self.ui.button_about,
                                        self.ui.button_options])
        # Set buttons with always show image
        for button in [self.ui.button_turnon]:
            button.set_always_show_image(True)
        # Set buttons as suggested
        self.set_buttons_style_suggested_action(
            buttons=[self.ui.button_turnon])
        # Set various properties
        self.ui.window.set_title(APP_NAME)
        self.ui.window.set_icon_from_file(str(FILE_ICON))
        self.ui.window.set_application(self.application)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        # Load settings
        for setting_name, action in self.settings_map.items():
            action.set_active(self.settings.get_preference(
                option=setting_name))
        # Load hosts
        self.settings.load_hosts(model=self.model_machines,
                                 icon=self.icon_empty)
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.window,
                                              section=SECTION_WINDOW_NAME)

    def run(self):
        """Show the UI"""
        logging.debug(f'{self.__class__.__name__} run')
        if self.options.autotest:
            GLib.timeout_add(500, self.do_autotests)
        self.ui.window.show_all()

    def do_autotests(self):
        """Perform a series of autotests"""
        # Show the information dialog
        for i in range(3):
            self.ui.action_about.activate()
            process_events()
            time.sleep(0.2)
        # Show the add host dialog
        for i in range(1, 4):
            self.detail.do_load_data(f'testing {i}',
                                     format_mac_address((str(i)) * 16),
                                     i, BROADCAST_ADDRESS)
            self.detail.show()
            process_events()
            time.sleep(0.2)
        # Show the ARP cache dialog
        for i in range(3):
            self.ui.action_import_arp_cache.activate()
            process_events()
            time.sleep(0.2)
        process_events()
        time.sleep(0.5)
        # Close the main window
        self.ui.window.destroy()

    def do_turn_on(self, treeiter):
        """Turn on the machine for the specified TreeIter"""
        mac_address = self.model_machines.get_mac_address(treeiter=treeiter)
        port_number = self.model_machines.get_port_number(treeiter=treeiter)
        destination = self.model_machines.get_destination(treeiter=treeiter)
        try:
            wake_on_lan(mac_address=mac_address,
                        port_number=port_number,
                        destination=destination)
            self.model_machines.set_icon(treeiter=treeiter,
                                         value=self.icon_yes)
        except OSError as error:
            logging.error(f'Unable to turn on: {mac_address} '
                          f'through {destination} '
                          f'using port number {port_number}')
            logging.error(error)
            self.model_machines.set_icon(treeiter=treeiter,
                                         value=self.icon_no)

    def on_action_about_activate(self, widget):
        """Show the information dialog"""
        dialog = UIAbout(parent=self.ui.window,
                         settings=self.settings,
                         options=self.options)
        dialog.show()
        dialog.destroy()

    def on_action_shortcuts_activate(self, widget):
        """Show the shortcuts dialog"""
        dialog = UIShortcuts(parent=self.ui.window,
                             settings=self.settings,
                             options=self.options)
        dialog.show()

    def on_action_quit_activate(self, widget):
        """Save the settings and close the application"""
        logging.debug(f'{self.__class__.__name__} quit')
        self.settings.save_window_position(window=self.ui.window,
                                           section=SECTION_WINDOW_NAME)
        self.settings.save_hosts(self.model_machines)
        self.settings.save()
        self.ui.window.destroy()
        self.detail.destroy()
        self.application.quit()

    def on_action_options_menu_activate(self, widget):
        """Open the options menu"""
        self.ui.button_options.clicked()

    def on_action_add_activate(self, widget):
        """Add a new empty machine"""
        self.detail.do_load_data(machine_name='',
                                 mac_address='',
                                 portnr=DEFAULT_UDP_PORT,
                                 destination=BROADCAST_ADDRESS)
        # Check if the OK button in the dialog was pressed
        if self.detail.show() == Gtk.ResponseType.OK:
            self.model_machines.add_data(
                MachineItem(
                    name=self.detail.do_get_machine_name(),
                    mac_address=self.detail.do_get_mac_address(),
                    port_number=self.detail.do_get_port_number(),
                    destination=self.detail.do_get_destination(),
                    icon=self.icon_empty))
            # Automatically select the last inserted item
            self.ui.treeview_machines.set_cursor(
                self.model_machines.count() - 1)

    def on_action_edit_activate(self, widget):
        """Edit the selected machine"""
        treeiter = get_treeview_selected_row(self.ui.treeview_machines)
        if treeiter:
            self.detail.do_load_data(
                self.model_machines.get_machine_name(treeiter=treeiter),
                self.model_machines.get_mac_address(treeiter=treeiter),
                self.model_machines.get_port_number(treeiter=treeiter),
                self.model_machines.get_destination(treeiter=treeiter)
            )
            if self.detail.show() == Gtk.ResponseType.OK:
                self.model_machines.set_machine_name(
                    treeiter=treeiter,
                    value=self.detail.do_get_machine_name())
                self.model_machines.set_mac_address(
                    treeiter=treeiter,
                    value=self.detail.do_get_mac_address())
                self.model_machines.set_port_number(
                    treeiter=treeiter,
                    value=self.detail.do_get_port_number())
                self.model_machines.set_destination(
                    treeiter=treeiter,
                    value=self.detail.do_get_destination())

    def on_action_delete_activate(self, widget):
        """Delete the selected machine"""
        treeiter = get_treeview_selected_row(self.ui.treeview_machines)
        if treeiter:
            # Ask confirmation to delete the selected machine
            if show_message_dialog_yesno(
                self.ui.window,
                _('Are you sure you want to remove the selected machine?'),
                _('Delete machine'),
                Gtk.ResponseType.NO
            ) == Gtk.ResponseType.YES:
                # Delete the selected machine
                self.model_machines.remove(treeiter)

    def on_action_turnon_activate(self, widget):
        """Launch the Wake On LAN for all the selected machines"""
        selected_count = 0
        for treeiter in self.model_machines:
            self.model_machines.set_icon(treeiter=treeiter,
                                         value=self.icon_empty)
        for treeiter in self.model_machines:
            # Turn on any selected machine
            if self.model_machines.get_selected(treeiter=treeiter):
                selected_count += 1
                self.do_turn_on(treeiter)
        if selected_count == 0:
            # When no machines are selected use the currently selected row
            treeiter = get_treeview_selected_row(self.ui.treeview_machines)
            if treeiter:
                self.do_turn_on(treeiter)

    def on_action_import_arp_cache_activate(self, widget):
        """Show the ARP cache picker dialog"""
        dialog = UIArpCache(parent=self.ui.window,
                            settings=self.settings,
                            options=self.options)
        # Check if the OK button in the dialog was pressed
        if dialog.show() == Gtk.ResponseType.OK:
            # Check if a valid machine with MAC Address was selected
            if dialog.do_get_mac_address():
                # Add the machine to the model from the ARP cache
                self.model_machines.add_data(
                    MachineItem(name=dialog.do_get_ip_address(),
                                mac_address=dialog.do_get_mac_address(),
                                port_number=DEFAULT_UDP_PORT,
                                destination=BROADCAST_ADDRESS,
                                icon=self.icon_empty))
                # Select the last machine and edit its details
                self.ui.treeview_machines.set_cursor(
                    self.model_machines.count() - 1)
                self.ui.action_edit.activate()
        # Destroy the dialog
        dialog.destroy()

    def on_action_import_ethers_activate(self, widget):
        """Show the Ethers file importer"""
        # noinspection PyArgumentList
        dialog = Gtk.FileChooserDialog(
            text(message='Select a File',
                 gtk30=True),
            None,
            Gtk.FileChooserAction.OPEN,
            (text(message='_Cancel', gtk30=True), Gtk.ResponseType.CANCEL,
             text(message='_Open', gtk30=True), Gtk.ResponseType.OK))
        dialog.set_transient_for(self.ui.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            importer = ImportEthers(BROADCAST_ADDRESS)
            importer.import_file(filepath=dialog.get_filename(),
                                 model=self.model_machines,
                                 icon=self.icon_empty)
        dialog.destroy()

    def on_action_select_all_activate(self, widget):
        for treeiter in self.model_machines:
            self.model_machines.set_selected(treeiter=treeiter,
                                             value=True)

    def on_action_deselect_all_activate(self, widget):
        for treeiter in self.model_machines:
            self.model_machines.set_selected(treeiter=treeiter,
                                             value=False)

    def on_cell_selected_toggled(self, renderer, treeiter, data=None):
        """Select or deselect an item"""
        self.model_machines.set_selected(
            treeiter=treeiter,
            value=not self.model_machines.get_selected(treeiter=treeiter))

    def on_treeview_machines_button_release_event(self, widget, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            self.ui.menu_select_machines.popup_at_pointer(event)

    def on_treeview_machines_row_activated(self, widget, path, column):
        """The double click on a row acts as the Edit machine button"""
        self.ui.action_edit.activate()

    def on_window_delete_event(self, widget, event):
        """Close the application by closing the main window"""
        self.ui.action_quit.activate()
