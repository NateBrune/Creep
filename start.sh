#!/bin/bash
./buildstatic.sh
./hia-iplist.sh
rm hia.iplist.*
rm hia-iplist.log
touch nis.log
python niscan.py hia.iplist
python nicrawl.py nis.log
