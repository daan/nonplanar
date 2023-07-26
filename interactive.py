import time
import sys
import serial
from serial_device import *
import math


print_ports()

print("connecting to the einsy")

devices = get_ports_with_vid(10161)
print(devices)
p = Printer()
p.open(devices[-1], baud=250000)

time.sleep(1.0)
while True:
    s = p.readline()
    if s == None:
        print("printer init done")
        break
    else:
        print(s)

p.home()
p.wait_for_ok()

print("homing done")

min_height = 10
height = min_height
target_height = height
radius = 25


p.move(100, 100, height, speed=3000)
p.wait_for_ok()

print("connecting to the RP2040")
rp2040 = SerialDevice()
rp2040.open(get_ports_with_vid(9114)[-1])


i = 0

while 1:
    i = (i + 1) % 36
    x = 100 + radius * math.cos(math.radians(i * 10))
    y = 100 + radius * math.sin(math.radians(i * 10))
    if target_height > height:
        height = min(target_height, height + 0.5)
    if target_height < height:
        height = max(target_height, height - 0.5)

    p.move(x, y, height, speed=3000)
    p.wait_for_ok()

    print(height, target_height)

    new_height = rp2040.readline()
    if new_height != None:
        target_height = min_height + float(new_height) * 50
        print(float(new_height))
