import time
import sys
import serial
from math import sin, pi
from serial_device import *
import rotaryio
import board

flow_encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)
last_flow_position = None
speed_encoder = rotaryio.IncrementalEncoder(board.D8, board.D7)
last_speed_position = None

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

    flow_position = flow_encoder.position 
    if last_flow_position is None or flow_position != last_flow_position:
        print("Flow " + flow_position + "\n")
    last_flow_position = flow_position

    speed_position = flow_encoder.position 
    if last_speed_position is None or speed_position != last_speed_position:
        print("Slow " + speed_position + "\n")
    last_speed_position = speed_position


#     if l != None:
#         target_height = 50 + float(l) * 50
#         print(height, target_height)
#     if target_height > height:
#         height = min(target_height, height + 0.1)
#         print(height, target_height)

#     if target_height < height:
#         height = max(target_height, height - 0.1)
#         print(height, target_height)
