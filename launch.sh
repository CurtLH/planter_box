#!/bin/sh

sleep 10

cd /home/pi/planter_box
/usr/bin/python ./monitor_temp.py >> /home/pi/log.txt 2>&1

