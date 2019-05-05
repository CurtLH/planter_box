#!/usr/bin/env python
import logging
import psycopg2
import ds18b20
from datetime import datetime
import json
from time import sleep

# connect to the databse
conn = psycopg2.connect(database="curtis",
                        user="curtis",
                        password="apassword",
                        host="192.168.0.110")

conn.autocommit = True
cur = conn.cursor()
logging.warning("Successfully connect to the database")

# create table
cur.execute("""CREATE TABLE IF NOT EXISTS temps
               (id SERIAL PRIMARY KEY NOT NULL,
                datetime timestamp UNIQUE NOT NULL,
                sensors jsonb)""")

# get temp sensors
sensors = ds18b20.get_sensors()
logging.warning("{} sensors identified".format(len(sensors)))

# read sensors on loop
while True:

    # get the current datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # read the temperature sensors
    temps = ds18b20.read_multiple_sensors(sensors)
    logging.warning(temps)

    # insert temps into database
    try:
        cur.execute("""INSERT INTO temps
                        (datetime, sensors)
                        VALUES (%s, %s)""", [now, json.dumps(temps)])
        logging.warning("New record inserted into database")
    except:
        pass
        logging.warning("Duplicate record identified")

    # wait then do it again
    sleep(300)
