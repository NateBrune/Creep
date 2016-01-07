#!/bin/bash
./hia-iplist.sh
rm hia.iplist.*
rm hia-iplist.log
touch nis.log
python niscan.py hia.iplist
touch creep.php
python nicrawl.py nis.log
