import time
import sys
import serial
from serial_device import *

devices = get_ports_with_vid(9114)

print("connecting to the RP2040")
rp2040 = SerialDevice()
rp2040.open(devices[-1])

height = 50
target_height = 50

while 1:
    l = rp2040.readline()
    if l != None:
        target_height = 50 + float(l) * 50
    print(height, target_height)
    if target_height > height:
        height = min(target_height, height + 0.1)
    if target_height < height:
        height = max(target_height, height - 0.1)
