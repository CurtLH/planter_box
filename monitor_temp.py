#!/usr/bin/env python
import logging
from time import sleep
import ds18b20
import requests

# set the parameters for dweet
url = "https://dweet.io/dweet/for/curtis-planter-box"

# get temp sensors
sensors = ds18b20.get_sensors()
logging.warning("{} sensors identified".format(len(sensors)))

# read sensors on loop
while True:

    # read the temperature sensors
    temps = ds18b20.read_multiple_sensors(sensors)
    logging.warning(temps)

    # send a message with the data
    r = requests.get(url, params=temps)

    # check the status of the request
    if r.status_code == 200:
        logging.warning("dweet successfully sent")
    else:
        logging.warning("dweet not successful ({})".format(r.status_code))

    # wait 30 seconds then do it again
    sleep(30)
