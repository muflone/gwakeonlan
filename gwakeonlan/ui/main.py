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

import time

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from gi.repository import Gtk

from gwakeonlan.constants import (FILE_ICON,
                                  APP_NAME,
                                  BROADCAST_ADDRESS, DEFAULT_UDP_PORT,
                                  FILE_SETTINGS)
from gwakeonlan.functions import (_,
                                  format_mac_address,
                                  get_pixbuf_from_icon_name,
                                  get_treeview_selected_row,
                                  get_ui_file,
                                  process_events,
                                  show_message_dialog_yesno,
                                  text,
                                  text_gtk30,
                                  wake_on_lan)
from gwakeonlan.gtkbuilder_loader import GtkBuilderLoader
from gwakeonlan.import_ethers import ImportEthers
from gwakeonlan.settings import Settings

from gwakeonlan.models.machine_item import MachineItem
from gwakeonlan.models.machines import ModelMachines

from gwakeonlan.ui.about import UIAbout
from gwakeonlan.ui.arpcache import UIArpCache
from gwakeonlan.ui.detail import UIDetail
from gwakeonlan.ui.shortcuts import UIShortcuts

SECTION_WINDOW_NAME = 'main window'


class UIMain(object):
    def __init__(self, application, options):
        """Prepare the main window"""
        self.application = application
        self.load_ui()
        self.settings = Settings(FILE_SETTINGS, True)
        self.options = options
        self.settings.restore_window_position(window=self.ui.window,
                                              section=SECTION_WINDOW_NAME)
        # Initialize actions
        for widget in self.ui.get_objects_by_type(Gtk.Action):
            # Connect the actions accelerators
            widget.connect_accelerator()
        # Load icons
        self.icon_empty = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,
                                               True, 8, 24, 24)
        self.icon_empty.fill(0)
        self.icon_yes = get_pixbuf_from_icon_name('gtk-yes', 24)
        # Load hosts
        self.settings.load_hosts(model=self.model,
                                 icon=self.icon_empty)
        # Load the others dialogs
        self.detail = UIDetail(self.ui.window, self.settings, options)
        self.detected_addresses = {}

    def run(self):
        """Show the main window"""
        if self.options.autotest:
            GLib.timeout_add(500, self.do_autotests)
        self.ui.window.show_all()

    def load_ui(self):
        """Load the UI for the main window"""
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('main.ui'))
        self.model = ModelMachines(self.ui.model)
        # Initialize translations
        self.ui.action_about.set_label(text_gtk30('About'))
        self.ui.action_shortcuts.set_label(text_gtk30('Shortcuts'))
        self.ui.action_select_all.set_label(text_gtk30('Select _All'))
        # Initialize actions
        for widget in self.ui.get_objects_by_type(Gtk.Action):
            # Connect the actions accelerators
            widget.connect_accelerator()
            # Set labels
            label = widget.get_label()
            if not label:
                label = widget.get_short_label()
            widget.set_label(text(label))
            widget.set_short_label(label)
        # Initialize labels
        for widget in self.ui.get_objects_by_type(Gtk.Label):
            widget.set_label(text(widget.get_label()))
        # Initialize tooltips
        for widget in self.ui.get_objects_by_type(Gtk.Button):
            action = widget.get_related_action()
            if action:
                widget.set_tooltip_text(action.get_label().replace('_', ''))
        # Initialize Gtk.HeaderBar
        self.ui.header_bar.props.title = self.ui.window.get_title()
        self.ui.window.set_titlebar(self.ui.header_bar)
        for button in (self.ui.button_turnon,
                       self.ui.button_add,
                       self.ui.button_edit,
                       self.ui.button_delete,
                       self.ui.button_about,
                       self.ui.button_options):
            action = button.get_related_action()
            if button in (self.ui.button_options, ):
                icon_size = Gtk.IconSize.BUTTON
            else:
                icon_size = Gtk.IconSize.LARGE_TOOLBAR
            button.set_image(Gtk.Image.new_from_icon_name(
                icon_name=action.get_icon_name(),
                size=icon_size))
            if not action.get_is_important():
                # Remove the button label
                button.props.label = None
            # Set the tooltip from the action label
            button.set_tooltip_text(action.get_label().replace('_', ''))
        # Set buttons with always show image
        for button in (self.ui.button_turnon, ):
            button.set_always_show_image(True)
        # Set various properties
        self.ui.window.set_title(APP_NAME)
        self.ui.window.set_icon_from_file(str(FILE_ICON))
        self.ui.window.set_application(self.application)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def do_autotests(self):
        """Perform a series of autotests"""
        # Show the about dialog
        for i in range(3):
            self.ui.action_about.emit('activate')
            process_events()
            time.sleep(0.2)
        # Show the add host dialog
        for i in range(1, 4):
            self.detail.load_data('testing %d' % i,
                                  format_mac_address(('%d' % i) * 16),
                                  i, BROADCAST_ADDRESS)
            self.detail.show()
            process_events()
            time.sleep(0.2)
        # Show the ARP cache dialog
        for i in range(3):
            self.ui.action_import_arp_cache.emit('activate')
            process_events()
            time.sleep(0.2)
        process_events()
        time.sleep(0.5)
        # Close the main window
        self.ui.window.destroy()

    def on_window_delete_event(self, widget, event):
        """Close the application by closing the main window"""
        self.ui.action_quit.emit('activate')

    def on_action_about_activate(self, widget):
        """Show the about dialog"""
        about = UIAbout(parent=self.ui.window,
                        settings=self.settings,
                        options=self.options)
        about.show()
        about.destroy()

    def on_action_shortcuts_activate(self, action):
        """Show the shortcuts dialog"""
        dialog = UIShortcuts(self.ui.window)
        dialog.show()

    def on_action_quit_activate(self, action):
        """Quit the application"""
        self.detail.destroy()
        self.settings.save_window_position(self.ui.window, SECTION_WINDOW_NAME)
        self.settings.save_hosts(self.model)
        self.settings.save()
        self.ui.window.destroy()
        self.application.quit()

    def on_action_add_activate(self, widget):
        """Add a new empty machine"""
        self.detail.load_data(machine_name='',
                              mac_address='',
                              portnr=DEFAULT_UDP_PORT,
                              destination=BROADCAST_ADDRESS)
        # Check if the OK button in the dialog was pressed
        if self.detail.show() == Gtk.ResponseType.OK:
            self.model.add_data(
                MachineItem(
                    name=self.detail.get_machine_name(),
                    mac_address=self.detail.get_mac_address(),
                    port_number=self.detail.get_port_number(),
                    destination=self.detail.get_destination(),
                    icon=self.icon_empty))
            # Automatically select the last inserted item
            self.ui.treeview_machines.set_cursor(self.model.count() - 1)

    def on_action_edit_activate(self, widget):
        """Edit the selected machine"""
        treeiter = get_treeview_selected_row(self.ui.treeview_machines)
        if treeiter:
            self.detail.load_data(
                self.model.get_machine_name(treeiter),
                self.model.get_mac_address(treeiter),
                self.model.get_port_number(treeiter),
                self.model.get_destination(treeiter)
            )
            if self.detail.show() == Gtk.ResponseType.OK:
                self.model.set_machine_name(treeiter,
                                            self.detail.get_machine_name())
                self.model.set_mac_address(treeiter,
                                           self.detail.get_mac_address())
                self.model.set_port_number(treeiter,
                                           self.detail.get_port_number())
                self.model.set_destination(treeiter,
                                           self.detail.get_destination())

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
                self.model.remove(treeiter)

    def on_action_turnon_activate(self, widget):
        """Launch the Wake On LAN for all the selected machines"""
        selected_count = 0
        for treeiter in self.model:
            self.model.set_icon(treeiter, self.icon_empty)
        for treeiter in self.model:
            if self.model.get_selected(treeiter):
                # If a machine was selected then it will turned on
                selected_count += 1
                wake_on_lan(
                    mac_address=self.model.get_mac_address(treeiter),
                    port_number=self.model.get_port_number(treeiter),
                    destination=self.model.get_destination(treeiter))
                self.model.set_icon(treeiter, self.icon_yes)
        if selected_count == 0:
            # When no machines are selected use the currently selected row
            treeiter = get_treeview_selected_row(self.ui.treeview_machines)
            if treeiter:
                wake_on_lan(
                    mac_address=self.model.get_mac_address(treeiter),
                    port_number=self.model.get_port_number(treeiter),
                    destination=self.model.get_destination(treeiter))
                self.model.set_icon(treeiter, self.icon_yes)

    def on_action_import_arp_cache_activate(self, widget):
        """Show the ARP cache picker dialog"""
        dialog = UIArpCache(parent=self.ui.window,
                            settings=self.settings,
                            options=self.options)
        # Check if the OK button in the dialog was pressed
        if dialog.show() == Gtk.ResponseType.OK:
            # Check if a valid machine with MAC Address was selected
            if dialog.get_mac_address():
                # Add the machine to the model from the ARP cache
                self.model.add_data(
                    MachineItem(name=dialog.get_ip_address(),
                                mac_address=dialog.get_mac_address(),
                                port_number=DEFAULT_UDP_PORT,
                                destination=BROADCAST_ADDRESS,
                                icon=self.icon_empty))
                # Select the last machine and edit its details
                self.ui.treeview_machines.set_cursor(self.model.count() - 1)
                self.ui.action_edit.emit('activate')
        # Destroy the dialog
        dialog.destroy()

    def on_action_import_ethers_activate(self, widget):
        """Show the Ethers file importer"""
        dialog = Gtk.FileChooserDialog(
            text_gtk30("Select a File"),
            None,
            Gtk.FileChooserAction.OPEN,
            (text_gtk30("_Cancel"), Gtk.ResponseType.CANCEL,
             text_gtk30("_Open"), Gtk.ResponseType.OK))
        dialog.set_transient_for(self.ui.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            importer = ImportEthers(BROADCAST_ADDRESS)
            importer.import_file(filepath=dialog.get_filename(),
                                 model=self.model,
                                 icon=self.icon_empty)
        dialog.destroy()

    def on_action_select_all_activate(self, widget):
        for treeiter in self.model:
            self.model.set_selected(treeiter, True)

    def on_action_deselect_all_activate(self, widget):
        for treeiter in self.model:
            self.model.set_selected(treeiter, False)

    def on_cell_selected_toggled(self, renderer, treeIter, data=None):
        """Select or deselect an item"""
        self.model.set_selected(
            treeIter,
            not self.model.get_selected(treeIter))

    def on_treeview_machines_button_release_event(self, widget, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            self.ui.menu_select_machines.popup_at_pointer(event)

    def on_treeview_machines_row_activated(self, widget, path, column):
        """The double click on a row acts as the Edit machine button"""
        self.ui.action_edit.emit('activate')
