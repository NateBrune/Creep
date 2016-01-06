#!/bin/bash
./hia-iplist.sh
rm hia.iplist.*
rm hia-iplist.log
touch nis.log
python2 niscan.py hia.iplist
touch creep.php
python2 nicrawl.py nis.log
