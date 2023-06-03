##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
# Proj Author: Fabio Castelli (Muflone) <muflone@muflone.com>
# File Author: Mohammad Bahoosh (Moisrex) <moisrex@gmail.com>
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
import paramiko
import logging
import socket


class Mikrotik:

    def wol(self, mac_address, username, router, interface, password):
        """Ask a Mikrotik router to turn on the machine on your behalf"""
        logging.info(f'Asking: {router} '
                     f'to turning on: {mac_address} '
                     f'in interface {interface}')
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(router, username=username, password=password)

            # Command can be found here:
            # https://wiki.mikrotik.com/wiki/Manual:Tools/Wake_on_lan
            stdin = None
            stdout = None
            stderr = None
            if interface == "":
                stdin, stdout, stderr = ssh.exec_command(f"/tool/wol mac=\"{mac_address}\"")
            else:
                stdin, stdout, stderr = ssh.exec_command(f"/tool/wol mac=\"{mac_address}\" interface=\"{interface}\"")
            if stdout:
                logging.info(f'{router} returned: {stdout.read()}')
            ssh.close()
            return True
        except paramiko.SSHException as err:
            msg = f'Failed to connect to router {router}, error: {err}'
            logging.error(msg)
            return msg
        except socket.gaierror as err:
            msg = f"Can't connect to {router}; {err}"
            logging.error(msg)
            return msg
