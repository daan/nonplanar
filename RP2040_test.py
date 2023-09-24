import time
import sys
import serial
from math import sin, pi
from serial_device import *

devices = get_ports_with_vid(9114)

print("connecting to the RP2040")
rp2040 = SerialDevice()
rp2040.open(devices[-1])

t_last = time.time()

position = 60 # mm
amplitude = 30  # in mm
period = 1.0  # in seconds

while 1:
    l = rp2040.readline_bytes()
    if l != None:
        try:
            position = float(l)
            print(position)
        except (ValueError, TypeError):
            pass

    t = time.time()
    if t > t_last + 0.01:
        t_last = t
        v = position + amplitude* sin((divmod(t,period)[1]/period) * 2 * pi)        
        rp2040.write(f"{v:.2f}\n")
