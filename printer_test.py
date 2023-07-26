import time
import serial
from serial_device import *
import math


print("connecting to the einsy")
print_ports()

devices = get_ports_with_vid(10161)
print(devices)


p = Printer()
p.open(devices[-1], baud=250000)

time.sleep(1.0)
while True:
    s = p.readline()
    if s == None:
        print("init done")
        break
    else:
        print(s)

p.home()
p.wait_for_ok()
p.move(100, 100, 50, speed=3000)
p.wait_for_ok()

i = 0

while 1:
    radius = 25
    x = 100 + radius * math.cos(math.radians(i * 10))
    y = 100 + radius * math.sin(math.radians(i * 10))
    p.move(x, y, 50, speed=3000)
    p.wait_for_ok()
    i = (i + 1) % 36
