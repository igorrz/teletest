import os
import glob
import time
from datetime import datetime
import csv

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
data_time_directory='home/pi/teletest/temp_measure/'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
	
while True:
    now=datetime.now()
    current_time=now().strftime("%H:%M")
    current_date = now.strftime("%d-%b")
    data=[current_date,current_time,read_temp()]
    with open(data_time_directory+'date_time_temp.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)
    time.sleep(2)

