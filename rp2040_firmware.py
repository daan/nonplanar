import board
import digitalio
import analogio
import time
from math import fabs

# crap circuitpython no ticks_ms()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pot = analogio.AnalogIn(board.A0)

# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
last_value = pot.value / 65535

# TODO: documentation says it does not work after one hour!!!
t_last = time.monotonic()

while True:
    value = pot.value / 65535
    if fabs(last_value - value) > 0.01:
        print(f"{pot.value / 65535:.2f}")
        last_value = value

    # heartbeat: blink led to show things are running
    t = time.monotonic()
    if t > t_last + 1:
        t_last = t
        led.value = not led.value
