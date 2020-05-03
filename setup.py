#!/usr/bin/env python2
##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2020 Fabio Castelli
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

from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data
from distutils.log import info

import os
import os.path
import shutil
from itertools import chain
from glob import glob

from gwakeonlan.constants import *


class Install_Scripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        "Rename main executable python script without .py extension"
        for script in self.get_outputs():
            if script.endswith(".py"):
                info('renaming the python script %s -> %s' % (
                    script, script[:-3]))
                shutil.move(script, script[:-3])


class Install_Data(install_data):
    def run(self):
        self.install_icons()
        self.install_translations()
        install_data.run(self)

    def install_icons(self):
        info('Installing icons...')
        DIR_ICONS = 'icons'
        for icon_format in os.listdir(DIR_ICONS):
            icon_dir = os.path.join(DIR_ICONS, icon_format)
            self.data_files.append((
                os.path.join('share', 'icons', 'hicolor', icon_format, 'apps'),
                glob(os.path.join(icon_dir, '*'))))

    def install_translations(self):
        info('Installing translations...')
        for po in glob(os.path.join('po', '*.po')):
            lang = os.path.basename(po[:-3])
            mo = os.path.join('build', 'mo', lang, '%s.mo' % DOMAIN_NAME)

            directory = os.path.dirname(mo)
            if not os.path.exists(directory):
                info('creating %s' % directory)
                os.makedirs(directory)

            cmd = 'msgfmt -o %s %s' % (mo, po)
            info('compiling %s -> %s' % (po, mo))
            if os.system(cmd) != 0:
                raise SystemExit('Error while running msgfmt')

            dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            self.data_files.append((dest, [mo]))

setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    maintainer=APP_AUTHOR,
    maintainer_email=APP_AUTHOR_EMAIL,
    url=APP_URL,
    description=APP_DESCRIPTION,
    license='GPL v2',
    scripts=['gwakeonlan.py'],
    packages=['gwakeonlan'],
    data_files=[
        ('share/gwakeonlan/data', ['data/gwakeonlan.png']),
        ('share/applications', ['data/gwakeonlan.desktop']),
        ('share/doc/gwakeonlan', list(chain(glob('doc/*'),  glob('*.md')))),
        ('share/man/man1', ['man/gwakeonlan.1']),
        ('share/gwakeonlan/ui', glob('ui/*')),
    ],
    cmdclass={
        'install_scripts': Install_Scripts,
        'install_data': Install_Data
    }
)
