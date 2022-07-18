#!/bin/bash

ifconfig eth0 10.10.0.1
udhcpd -f
/usr/bin/python3 /home/revolnoom/serverOdroid.py &
