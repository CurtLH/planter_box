#!/usr/bin/env python
import logging
import requests
import psycopg2
import json
from time import sleep

# connect to the databse
conn = psycopg2.connect(database="curtis",
                        user="curtis",
                        password="apassword",
                        host="localhost")

conn.autocommit = True
cur = conn.cursor()
logging.warning("Successfully connect to the database")

# create table
cur.execute("""CREATE TABLE IF NOT EXISTS temps
               (id SERIAL PRIMARY KEY NOT NULL,
                created timestamp UNIQUE NOT NULL,
                temps jsonb)""")

# get the latest dweet
url = "https://dweet.io/get/latest/dweet/for/curtis-planter-box"

# continuosly look for new temperatures
while True:
    
    # get the latest dweet
    r = requests.get(url)
    logging.warning("Latest dweet obtained")

    # check the status code
    if r.status_code == 200:
        
        # parse the data
        data = r.json()['with'][0]
        
        # insert temps into database
        try:
            cur.execute("""INSERT INTO temps
                           (created, temps)
                           VALUES (%s, %s)""", [data['created'], 
                                                json.dumps(data['content'])])
            logging.warning("New record inserted into database")
        except:
            pass
            logging.warning("Duplicate record identified")
        
    sleep(30)
