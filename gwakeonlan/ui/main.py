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

from gi.repository import GLib
from gi.repository import Gtk

from gwakeonlan.constants import (FILE_ICON,
                                  APP_NAME,
                                  BROADCAST_ADDRESS, DEFAULT_UDP_PORT,
                                  FILE_SETTINGS)
from gwakeonlan.functions import (_,
                                  text_gtk30,
                                  show_message_dialog_yesno,
                                  formatMAC,
                                  get_ui_file,
                                  process_events,
                                  wake_on_lan)
from gwakeonlan.import_ethers import ImportEthers
from gwakeonlan.model_machines import ModelMachines
from gwakeonlan.settings import Settings

from gwakeonlan.ui.about import UIAbout
from gwakeonlan.ui.arpcache import UIArpCache
from gwakeonlan.ui.detail import DetailWindow

SECTION_WINDOW_NAME = 'main window'


class MainWindow(object):
    def __init__(self, application, options):
        """Prepare the main window"""
        self.application = application
        self.loadUI()
        self.settings = Settings(FILE_SETTINGS, True)
        self.options = options
        self.settings.restore_window_position(self.winMain, SECTION_WINDOW_NAME)
        self.settings.load_hosts(self.model)
        self.options = options
        # Load the others dialogs
        self.about = UIAbout(self.winMain, self.settings, options)
        self.detail = DetailWindow(self.winMain, self.settings, options, False)
        self.detected_addresses = {}

    def run(self):
        """Show the main window"""
        if self.options.autotest:
            GLib.timeout_add(500, self.do_autotests)
        self.winMain.show_all()

    def loadUI(self):
        """Load the UI for the main window"""
        builder = Gtk.Builder()
        builder.add_from_file(get_ui_file('main.glade'))
        # Obtain widget references
        self.winMain = builder.get_object("winMain")
        self.model = ModelMachines(builder.get_object('storeMachines'))
        self.btnAdd = builder.get_object('btnAdd')
        self.btnEdit = builder.get_object('btnEdit')
        self.btnDelete = builder.get_object('btnDelete')
        self.tvwMachines = builder.get_object('tvwMachines')
        # Set various properties
        self.winMain.set_title(APP_NAME)
        self.winMain.set_icon_from_file(str(FILE_ICON))
        self.winMain.set_application(self.application)
        # Connect signals from the glade file to the functions
        # with the same name
        builder.connect_signals(self)

    def on_winMain_delete_event(self, widget, event):
        """Close the application by closing the main window"""
        self.about.destroy()
        self.detail.destroy()
        self.settings.save_window_position(self.winMain, SECTION_WINDOW_NAME)
        self.settings.save_hosts(self.model)
        self.settings.save()
        self.winMain.destroy()
        self.application.quit()

    def on_btnAbout_clicked(self, widget):
        """Show the about dialog"""
        self.about.show()

    def on_cellMachinesSelected_toggled(self, renderer, treeIter, data=None):
        """Select or deselect an item"""
        self.model.set_selected(
            treeIter,
            not self.model.get_selected(treeIter))

    def on_btnAdd_clicked(self, widget):
        """Add a new empty machine"""
        self.detail.load_data('', '', DEFAULT_UDP_PORT, BROADCAST_ADDRESS)
        # Check if the OK button in the dialog was pressed
        if self.detail.show() == Gtk.ResponseType.OK:
            self.model.add_machine(
                False,
                self.detail.get_machine_name(),
                self.detail.get_mac_address(),
                self.detail.get_portnr(),
                self.detail.get_destination()
            )
            # Automatically select the last inserted item
            self.tvwMachines.set_cursor(self.model.count() - 1)

    def on_btnEdit_clicked(self, widget):
        """Edit the selected machine"""
        selected = self.tvwMachines.get_selection().get_selected()[1]
        if selected:
            self.detail.load_data(
                self.model.get_machine_name(selected),
                self.model.get_mac_address(selected),
                self.model.get_portnr(selected),
                self.model.get_destination(selected)
            )
            if self.detail.show() == Gtk.ResponseType.OK:
                self.model.set_machine_name(selected,
                                            self.detail.get_machine_name())
                self.model.set_mac_address(selected,
                                           self.detail.get_mac_address())
                self.model.set_portnr(selected,
                                      self.detail.get_portnr())
                self.model.set_destination(selected,
                                           self.detail.get_destination())

    def on_menuitemARPCache_activate(self, widget):
        """Show the ARP cache picker dialog"""
        dialog = UIArpCache(self.winMain, self.settings, self.options)
        # Check if the OK button in the dialog was pressed
        if dialog.show() == Gtk.ResponseType.OK:
            # Check if a valid machine with MAC Address was selected
            if dialog.get_mac_address():
                # Add the machine to the model from the ARP cache
                self.model.add_machine(
                    False,
                    dialog.get_ip_address(),
                    dialog.get_mac_address(),
                    DEFAULT_UDP_PORT,
                    BROADCAST_ADDRESS)
                # Select the last machine and edit its details
                self.tvwMachines.set_cursor(self.model.count() - 1)
                self.btnEdit.emit('clicked')

        # Destroy the dialog
        dialog.destroy()

    def on_tvwMachines_row_activated(self, widget, path, column):
        """The double click on a row acts as the Edit machine button"""
        self.btnEdit.emit('clicked')

    def on_menuitemImportEthers_activate(self, widget):
        """Show the Ethers file importer"""
        dialog = Gtk.FileChooserDialog(
            text_gtk30("Select a File"),
            None,
            Gtk.FileChooserAction.OPEN,
            (text_gtk30("_Cancel"), Gtk.ResponseType.CANCEL,
             text_gtk30("_Open"), Gtk.ResponseType.OK))
        dialog.set_transient_for(self.winMain)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            importer = ImportEthers(BROADCAST_ADDRESS)
            importer.import_file(dialog.get_filename(), self.model.add_machine)
        dialog.destroy()

    def on_btnDelete_clicked(self, widget):
        """Delete the selected machine"""
        selected_iter = self.tvwMachines.get_selection().get_selected()[1]
        if selected_iter:
            # Ask confirmation to delete the selected machine
            if show_message_dialog_yesno(
                self.winMain,
                _('Are you sure you want to remove the selected machine?'),
                _('Delete machine'),
                Gtk.ResponseType.NO
            ) == Gtk.ResponseType.YES:
                # Delete the selected machine
                self.model.remove(selected_iter)

    def on_btnWake_clicked(self, widget):
        """Launch the Wake On LAN for all the selected machines"""
        for machine in self.model:
            if self.model.get_selected(machine):
                # If a machine was selected then it will turned on
                wake_on_lan(
                    self.model.get_mac_address(machine),
                    self.model.get_portnr(machine),
                    self.model.get_destination(machine),
                    self.settings
                )

    def do_autotests(self):
        """Perform a series of autotests"""
        # Show the about dialog
        for i in range(3):
            self.on_btnAbout_clicked(None)
            process_events()
            time.sleep(0.2)
        # Show the add host dialog
        for i in range(1, 4):
            self.detail.load_data('testing %d' % i,
                                  formatMAC(('%d' % i) * 16),
                                  i, BROADCAST_ADDRESS)
            self.detail.show()
            process_events()
            time.sleep(0.2)
        # Show the ARP cache dialog
        for i in range(3):
            self.on_menuitemARPCache_activate(None)
            process_events()
            time.sleep(0.2)
        process_events()
        time.sleep(0.5)
        # Close the main window
        self.winMain.destroy()
