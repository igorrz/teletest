import os
import glob
import time
import datetime
import csv

today = date.today()
d4 = today.strftime("%b-%d-%Y")

print("Today's date:", today)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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
    today = datetime.date.today()
    current_time=datetime.now().strftime("%H:%M")
    date = today.strftime("%b-%d")
    data=[date,current_time,read_temp()]
    with open('date_time_temp.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)
	time.sleep(120)

data_time_directory='home/pi/teletest/temp_measure'