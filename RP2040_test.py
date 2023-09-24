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

rp2040.write("hello there\n")


while 1:
     l = rp2040.readline_bytes()
     if l != None:
        print()
        if ord(l[0]) == 97:
            rp2040.write("hello\n")
        else:
            print(f"read {l}")


#     if l != None:
#         target_height = 50 + float(l) * 50
#         print(height, target_height)
#     if target_height > height:
#         height = min(target_height, height + 0.1)
#         print(height, target_height)

#     if target_height < height:
#         height = max(target_height, height - 0.1)
#         print(height, target_height)
