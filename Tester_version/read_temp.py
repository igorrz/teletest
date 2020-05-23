import os
import glob
import time
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')