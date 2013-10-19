#!/usr/bin/env python2
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

from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data

import os
import os.path
import shutil
from glob import glob
from gwakeonlan.constants import *

class rename_python_scripts(install_scripts):
  "Rename main executable python script without .py extension"
  def run(self):
    install_scripts.run(self)
    for script in self.get_outputs():
      if script.endswith(".py"):
        shutil.move(script, script[:-3])

class install_icons(install_data):
  "Install icons in the hicolor theme directory"
  def run (self):
    DIR_ICONS = 'icons'
    for icon_format in os.listdir(DIR_ICONS):
      icon_dir = os.path.join(DIR_ICONS, icon_format)
      self.data_files.append((
        os.path.join('share', 'icons', 'hicolor', icon_format, 'apps'),
        glob(os.path.join(icon_dir, '*'))))
    install_data.run(self)

setup(
  name=APP_NAME,
  version=APP_VERSION,
  description=APP_DESCRIPTION,
  author=APP_AUTHOR,
  author_email=APP_AUTHOR_EMAIL,
  maintainer=APP_AUTHOR,
  maintainer_email=APP_AUTHOR_EMAIL,
  url=APP_URL,
  license='GPL v2',
  scripts=['gwakeonlan.py'],
  packages=['gwakeonlan'],
  data_files=[
    ('share/gwakeonlan/data', (
      'data/gwakeonlan.png',
    )),
    ('share/gwakeonlan/ui',
      glob('ui/*.glade')
    ),
    ('share/applications', (
      'data/gwakeonlan.desktop',
    ))
  ],
  cmdclass = {
    'install_scripts': rename_python_scripts,
    'install_data': install_icons
  }
)
