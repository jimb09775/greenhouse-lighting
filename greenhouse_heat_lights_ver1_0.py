#!/usr/bin/python
'''*****************************************************************************************************************
    Modified from
    Seeed Studio Relay Board Example
    By John M. Wargo
    www.johnwargo.com
********************************************************************************************************************'''
from __future__ import print_function

import sys
import time
import os
import glob
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = [glob.glob(base_dir + '28*')[0],glob.glob(base_dir + '28*')[1],glob.glob(base_dir + '28*')[2]]
device_file = (device_folder[0] +'/w1_slave', device_folder[1] +'/w1_slave', device_folder[2] +'/w1_slave')

from relay_lib_seeed import *

def read_temp_raw(device):
    f=open(device_file[device], 'r')
    lines=f.readlines()
    f.close()
    return lines

def read_temp(device):
    lines=read_temp_raw(device)
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
#SENSORS  
room_temp=0

#Relays
 
relay_heater = 1
relay_lights =2


def process_loop():
    
    print(read_temp(room_temp))
 
	
    # now cycle each relay every second in an infinite loop
    while True:

        # Loop to turn on lights
        if int(datetime.datetime.now().strftime("%H"))>18 and int(datetime.datetime.now().strftime("%H"))<23:  #only allowed to run at night
            print('after sundown lights are on')
            relay_on(relay_lights)
		else:
		    print('lights are off')
            relay_off(relay_lights)
		
        if(read_temp(room_temp) < 5:  #cold
            relay_on(relay_heater)
            print('heater on')
               
        else:
		 	relay_off(relay_heater)
            print('heater off)
                  
        
         
            
        print('room temperature is ',read_temp(room_temp), 'or in fahernheit',read_temp(room_temp)*9/5+32)
        print(datetime.datetime.now().strftime("%H"))
            
            


# Now see what we're supposed to do next
if __name__ == "__main__":
    try:
        process_loop()
    except KeyboardInterrupt:
        # tell the user what we're doing...
        print("\nExiting application")
        print("Stan says we are in ",__name__)
        # turn off all of the relays
        relay_all_off()
        # exit the application
        sys.exit(0)
