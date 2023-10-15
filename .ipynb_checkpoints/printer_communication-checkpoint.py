import time
import sys
import serial
from serial_device import *
import fullcontrol as fc
from create_gcode import *
import shapes as shape


# Initialize printer
print("connecting to the Ender")
print_ports()

devices = get_ports_with_vid(10161)
print(devices)

p = Printer()
p.open(devices[-1], baud=115200)

time.sleep(1.0)
while True:
    s = p.readline()
    if s == None:
        print("init done")
        break
    else:
        print(s)

p.send_gcode("G28")
p.wait_for_ok()

gcode = shape.line_wave(2)

for line in gcode:
    print(line)
    p.send_gcode(line)
    p.wait_for_ok()

