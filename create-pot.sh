#!/bin/bash
POTFILE="po/gwakeonlan.pot.new"

if [ -f ui/*.glade.h ]
then
  rm ui/*.glade.h
fi
for _gladefile in ui/*.glade
do
  intltool-extract --type=gettext/glade ${_gladefile}
done

if ! [ -f $POTFILE ]
then
  touch $POTFILE
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output $POTFILE ui/*.glade.h *.py gwakeonlan/*.py
rm ui/*.glade.h
