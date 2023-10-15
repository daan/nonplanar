import time
import sys
import serial
from serial_device import *
import fullcontrol as fc
import create_gcode as cg

z_range =  0.1 # fader val conversion -z_range to z_range (if custom mapping is on)
total_z = 0
gcode_line = 0 # Starts gcode at line 0
zval = 0
i = 0
gcode = []
gcode_path = "C:\\Users\\malbe\\OneDrive - TU Eindhoven\\1 Online Bureaublad\\GitHub\\nonplanar\\created gcode\\Oval.gcode"

def custom_mapping(value): #Maps from 0, 120 to -z_range to z_range 
    return (value / 60 - 1) * z_range


print_ports()
MP2040 = get_ports_with_vid(9114)
print("MP2040 device = ", MP2040)
print("connecting to the RP2040")
rp2040 = SerialDevice()
rp2040.open(MP2040[-1],baud=9600)

ENDER3 = get_ports_with_vid(6790)
print("MP2040 device = ", ENDER3)
p = Printer()
print("connecting to the Ender")
p.open(ENDER3[-1], baud=115200)

p.send_gcode("G28")
print('Homing..')
p.wait_for_ok()
time.sleep(1.0)

while True:
    s = p.readline()
    if s == None:
        print("init done")
        break
    else:
        print(s)

start_position = ('{}\n'.format(input('Type starting position here: '))) #Write start position to the fader
rp2040.write(start_position)
time.sleep(1.0)

with open(gcode_path, 'r') as file:
    for line in file:
        gcode_line = line.strip()
        if gcode_line:  # This condition checks if the line is not empty (it seems to stall serial communication)
            gcode.append(gcode_line)


# Only sends fader data to printer
# while 1: 
#     l = rp2040.readline_bytes()
#     if l != None:
#         print('raw sensor value  = ', l)
#         fader_val = (float(f"{l}"))*z_range
#         print('zval conversion = ', fader_val)
#         code = ('G0 F1000 Z{}'.format(fader_val)) # Moves Z-axis
#         p.send_gcode(code)
#         p.wait_for_ok


while 1: #Sends z coordinates seperate from gcode: not so smooth
    faderval = rp2040.readline_bytes()
    if faderval != None:
        print(faderval)
        zval = (float(f"{faderval}"))*z_range
        print('zval = ', zval)
    p.send_gcode('G0 F1000 Z{}'.format(zval)) # Travel to z height
    p.send_gcode(gcode[i])
    p.wait_for_ok()
    faderval = rp2040.readline_bytes()
    i = i  +1


# while 1: #Appends z directly to coordinates
#     faderval = rp2040.readline_bytes()
#     print(faderval)
#     if faderval != None:
#         print(faderval)
#         zval = (float(f"{faderval}"))*z_range
#         print('zval = ', zval)
#     adjusted_gcode = cg.adjust_z_height(gcode[i],zval)
#     p.send_gcode(adjusted_gcode)
#     p.wait_for_ok()
#     i=i+1











# if faderdiff < margin : adjust z_height
# Incremental zheight adjustment?
# Apply sine wave on contours of shoe?
# Send z back to the fader






# while 1:
#      l = rp2040.readline_bytes()
#      p.send_gcode(gcode[i])
#      print(gcode[i])
#      if l != None:
#         print(l)
#         fader_val = (float(f"{l}"))*z_range
#         print('faderval = ', fader_val)
#         code = ('G0 F1000 Z{}'.format(fader_val)) # Moves Z-axis
#         print('Total_z (absolute position) = ', fader_val)
#         p.send_gcode(code)
#      p.wait_for_ok()
#      i = i + 1

        
    