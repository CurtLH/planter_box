#!/usr/bin/env python
import logging
from time import sleep
import ds18b20
from datetime import datetime
import requests
import json

# set the parameters for dweet
url = "https://dweet.io/dweet/for/curtis-planter-box"

# get temp sensors
sensors = ds18b20.get_sensors()
logging.warning("{} sensors identified".format(len(sensors)))

# read sensors on loop
while True:

    # get the current datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # read the temperature sensor
    temp = ds18b20.read_sensor(sensors['sensor3'])

    # store the results as JSON
    data = json.dumps({'temp': temp, 'datetime': now})
    logging.warning(data)

    # send a message with the data
    r = requests.get(url, params=data)

    # check the status of the request
    if r.status_code == 200:
        logging.warning("dweet successfully sent")
    else:
        logging.warning("dweet not successful ({})".format(r.status_code))

    # wait 30 seconds then do it again
    sleep(30)
