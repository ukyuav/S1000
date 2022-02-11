#!/usr/bin/python3
import os
import time
import serial
import sys
from gpiozero import LED, Button

#check if Arduino ADC is connected via USB
#if not used, program continues with only iMET recording
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
    #print("No ADC attached. Not using.\n") #TODO
    use_ADC = 0

      
#ser_xBee = serial.Serial(
#        port='/dev/ttyS0',
#        baudrate = 9600,
#        parity=serial.PARITY_NONE,
#        stopbits=serial.STOPBITS_ONE,
#        bytesize=serial.EIGHTBITS,
#        timeout=1
#)

#check if iMet attached
try:
    ser_iMET = serial.Serial(
            port='/dev/imet',
            baudrate = 57600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
	)
except:
        print("no iMET attached, cannot continue. \n")
        exit()

try:
    collect_ADC = LED(27)
    stop_button = Button(25, pull_up=False) #TODO: was 25, changed to 13/17

    counter=0#potentially unneccessary

#open iMET file
#first get filename
    data_path = "/mnt/sda1/iMET_data/IMETDATA"
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
            iMET_file = open(data_file, "a+") #open new iMET file appending
            data_iMET = ser_iMET.readline().decode()
            collect_ADC.on() #tell arduino to grab data
            collect_ADC.off()
            data_ADC = ser_ADC.readline().decode()
	    #data_all = data_ADC + data_iMET
            #ser_xBee.write(data_all)
            iMET_file.write(data_iMET)
            iMET_file.write("\n")
            iMET_file.close()
		
        else:
        
            iMET_file = open(data_file, "a+") #open new iMET file appending
            data_iMET = ser_iMET.readline().decode()
            print(data_iMET) #TODO: remove
            iMET_file.write(data_iMET)
            iMET_file.write("\n")
            iMET_file.close()
    
#stop_button.wait_for_press()
#print("aye bro the button was pressed")
    """
    for x in range (10):
             #iMET_file = open(data_file, "a+") #open new iMET file appending
             data_iMET = ser_iMET.readline().decode()
             print(data_iMET)
             #iMET_file.write(data_iMET)
             #iMET_file.write("\n")
             #iMET_file.close()
    """
    print("done\n")
    
except:
    print("exception thrown")
    if not iMET_file.closed:
        print("closing file")
        iMET_file.close()
