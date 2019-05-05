#! /usr/bin/env python
import os
import glob

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def get_sensors():

    """look for what sensors are available"""

    # check directory to find which sensors are available
    base_dir = '/sys/bus/w1/devices/'
    devices = glob.glob(base_dir + "28*")

    # name and file path for all sensors
    sensor_ids = {'sensor1' : '/sys/bus/w1/devices/28-0415a45a31ff/w1_slave', 
                  'sensor2' : '/sys/bus/w1/devices/28-0415a44740ff/w1_slave',
                  'sensor3' : '/sys/bus/w1/devices/28-0415a455b8ff/w1_slave',
                  'sensor4' : '',
                  'sensor5' : ''}
    
    # get paths for only active sensors
    sensors = {}
    for sensor in sensor_ids:
        if sensor_ids[sensor][:35] in devices:
            sensors[sensor] = sensor_ids[sensor]

    return sensors


def read_sensor_raw(device_file):

    """return raw value from one sensor"""
    
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    
    return lines


def read_sensor(device_file):
    
    """parse raw value into temp"""

    lines = read_sensor_raw(device_file)
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_sensor_raw()
    equals_pos = lines[1].find('t=')
    
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        
        return round(temp_f, 1)


def read_multiple_sensors(sensors):

    """takes reading from all sensors"""

    # create an empty dict to add sensor readings to
    readings = {}
    
    # get readings for all sensor files within sensors
    for sensor in sensors.keys():
        readings[sensor] = read_sensor(sensors[sensor])

    return readings
