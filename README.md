gWakeOnLAN
==========
**Description:** Wake up your machines using Wake on LAN.

**Copyright:** 2009-2014 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**License:** GPL-2+

**Source code:** https://github.com/muflone/gwakeonlan

**Documentation:** http://url.muflone.com/gwakeonlan

System Requirements
-------------------

* Python 2.x (developed and tested for Python 2.7.5)
* XDG library for Python 2
* GTK+3.0 libraries for Python 2
* GObject libraries for Python 2
* Distutils library for Python 2 (usually shipped with Python distribution)

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python2 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python2 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python2 gwakeonlan.py

If the application was installed simply use the gwakeonlan command.
