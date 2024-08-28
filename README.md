# gWakeOnLAN

[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/gwakeonlan/master.svg)](https://circleci.com/gh/muflone/gwakeonlan)

**Description:** Wake up your machines using Wake on LAN

**Copyright:** 2009-2024 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/gwakeonlan/

**Documentation:** http://www.muflone.com/gwakeonlan/

**Translations:** https://explore.transifex.com/muflone/gwakeonlan/

# Description

From the *gWakeOnLAN* main window you can define your hosts along with their
MAC Addresses, select those you want to turn on and just start them with a
simple click on the button **Turn on**.

![Main window](http://www.muflone.com/resources/gwakeonlan/archive/latest/english/main.png)

For each host you can define its name, the MAC address and you can choose to
turn it on on the local network or via internet through a destination
host.

![Detail](http://www.muflone.com/resources/gwakeonlan/archive/latest/english/detail.png)

# System Requirements

* Python >= 3.6 (developed and tested for Python 3.9 and 3.10)
* XDG library for Python 3 ( https://pypi.org/project/pyxdg/ )
* GTK+ 3.0 libraries for Python 3
* GObject libraries for Python 3 ( https://pypi.org/project/PyGObject/ )

# Installation

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python3 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python3 setup.py install --root NEW_PATH

# Usage

If the application is not installed please use:

    cd /path/to/folder
    python3 gwakeonlan.py

If the application was installed simply use the gwakeonlan command.
