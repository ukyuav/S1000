#!/usr/bin/python3
import os
import time
import serial
import sys
from gpiozero import LED, Button

#check if Arduino ADC is connected via USB
#if not used, program continues with only iMET recording
"""
try:
    ser_ADC = serial.Serial(
            port='/dev/ARD',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2
    )
    use_ADC = 1
except: #error if no adc attached.
    print("No ADC attached for the GPS. Not using.\n") #TODO
    use_ADC = 0
"""

#check if GPS attached
try:
    ser_gps = serial.Serial('/dev/gps', 4800)
except:
        print("no GPS attached, cannot continue. \n")
        exit()
use_ADC = 1
try:
    #collect_ADC = LED(27)
    #stop_button = Button(25, pull_up=False) #TODO: was 25, changed to 13/17

#open GPS file
#first get filename
    data_path = "/mnt/sda1/GPS_data/GPS"
    #location = sys.argv[1]
    #init_iMET_filename = "IMETDATA"
    for i in range(100):
        to_append = str(i)+".CSV" #TODO was i
        data_file = data_path + to_append
        file_exists = os.path.isfile(data_file)
        if file_exists == 0: #if file doesn't exist exit loop and create it
			     #file is created in the following while loop
            break
    time.sleep(1)
    #print("launching while loop \n") #TODO
    
    temp = 1
    while(True):
        if use_ADC == 1:
            gps_file = open(data_file, "a+") #open new file appending
            data_gps = ser_gps.readline().decode()
           # collect_ADC.on() #tell arduino to grab data
           # collect_ADC.off()
           # data_ADC = ser_ADC.readline().decode()
            gps_file.write(data_gps)
            gps_file.write("\n")
            gps_file.close()
		
        else:
        
            gps_file = open(data_file, "a+") #open new iMET file appending
            data_gps = ser_gps.readline().decode()
            print(data_gps) #TODO: remove
            gps_file.write(data_gps)
            gps_file.write("\n")
            gps_file.close()
        
except:
    print("exception thrown")
    if gps_file is not None and not gps_file.closed:
        print("closing file")
        gps_file.close()
