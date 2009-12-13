#!/bin/bash
intltool-extract --type=gettext/glade ../ui/gwakeonlan.glade
if [ -f gwakeonlan.pot ]
then
  rm gwakeonlan.pot
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output gwakeonlan.pot ../ui/*.glade.h ../gwakeonlan
rm ../ui/*.glade.h
