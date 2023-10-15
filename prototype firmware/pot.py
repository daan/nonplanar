#
#   in circuit python use MU editor
#

import board
import digitalio
import analogio
import pwmio
import busio
import time
from math import fabs

# crap circuitpython no ticks_ms()

uart = busio.UART(board.TX, board.RX, baudrate=9600)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pot = analogio.AnalogIn(board.A0)


# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
last_value = pot.value / 65535

t_last = time.monotonic()

target = 32535

while True:
    value = pot.value / 65535
    if fabs(last_value - value) > 0.02:
        print(f"{pot.value / 65535:.2f}")
        last_value = value
    t = time.monotonic()
    # heartbeat
    if t > t_last + 0.5:
        t_last = t
        led.value = not led.value
