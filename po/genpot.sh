#!/bin/bash
if [ -f ../data/*.glade.h ]
then
  rm ../data/*.glade.h
fi
intltool-extract --type=gettext/glade ../data/gwakeonlan.glade

if ! [ -f gwakeonlan.pot ]
then
  touch gwakeonlan.pot
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output gwakeonlan.pot --join-existing ../data/*.glade.h ../gwakeonlan
rm ../data/*.glade.h
echo ok
read
