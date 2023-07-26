#
#   this is circuit python. upload with mu
#

import board
import digitalio
import analogio
import time
from math import fabs

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pot = analogio.AnalogIn(board.A0)

# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
last_value = pot.value / 65535

while True:
    value = pot.value / 65535
    if fabs(last_value - value) > 0.01:
        print(f"{pot.value / 65535:.2f}")
        last_value = value
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
