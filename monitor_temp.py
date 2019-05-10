#!/usr/bin/env python
import os
import logging
import psycopg2
import ds18b20
from datetime import datetime
import json
from time import sleep

# enable logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# connect to the databse
conn = psycopg2.connect(database="temps",
                        user=os.getenv("PSQL_USER"),
                        password=os.getenv("PSQL_PASSWORD"),
                        host=os.getenv("PSQL_HOST"))

conn.autocommit = True
cur = conn.cursor()
logging.info("Successfully connect to the database")

# create table
cur.execute("""CREATE TABLE IF NOT EXISTS temps
               (id SERIAL PRIMARY KEY NOT NULL,
                datetime timestamp UNIQUE NOT NULL,
                sensors jsonb)""")

# get temp sensors
sensors = ds18b20.get_sensors()
logging.info("{} sensors identified".format(len(sensors)))

# read sensors on loop
while True:

    # get the current datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # read the temperature sensors
    temps = ds18b20.read_multiple_sensors(sensors)
    logging.info(temps)

    # insert temps into database
    try:
        cur.execute("""INSERT INTO temps
                        (datetime, sensors)
                        VALUES (%s, %s)""", [now, json.dumps(temps)])
        logging.info("New record inserted into database")
    except:
        pass
        logging.info("Duplicate record identified")

    # wait then do it again
    sleep(300)
