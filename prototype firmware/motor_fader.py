#
#   in circuit python use MU editor
#

import board
import digitalio
import analogio
import pwmio
import busio
import touchio

import time
from math import fabs

# crap circuitpython no ticks_ms()
t_last = time.monotonic()

uart = busio.UART(board.TX, board.RX, baudrate=9600)

# heartbeat
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pot = analogio.AnalogIn(board.A0)
# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
last_value = pot.value / 65535


touch_pad = board.A1
touch = touchio.TouchIn(touch_pad)
# True when the knob is being touched.
last_touch_state = False


ain1 = digitalio.DigitalInOut(board.D24)
ain1.direction = digitalio.Direction.OUTPUT
ain2 = digitalio.DigitalInOut(board.D25)
ain2.direction = digitalio.Direction.OUTPUT
apwm = pwmio.PWMOut(board.D2)
apwm.duty_cycle = 0


def set_motor(speed):
    if speed < 0:
        ain1.value = True
        ain2.value = False
    else:
        ain1.value = False
        ain2.value = True
    apwm.duty_cycle = abs(speed)


target = 32000

#set_motor(-65535)
#time.sleep(0.1)

set_motor(65535)
time.sleep(0.1)
set_motor(0)


while True:
    if touch.value != last_touch_state:
        if last_touch_state:
            # user stopped touching
            #target = pot.value
            last_touch_state = False
            print("end touch")
        else:
            last_touch_state = True
            print("start touch")
    if touch.value:
        set_motor(0) # no motor when user touches
    else: 
        v = pot.value
        delta = abs(target - v)
        speed = 65535
        if delta > 500:
            if v < target:
                set_motor(speed)
            else:
                set_motor(-speed)
            print(f"move motor {v} {target}")
        else:
            set_motor(0)
            
    # print the value when touching
    if touch.value:
        value = pot.value / 65535
        if fabs(last_value - value) > 0.02:
            print(f"{pot.value / 65535:.2f}")
            last_value = value

    t = time.monotonic()
    # heartbeat
    if t > t_last + 0.5:
        t_last = t
        led.value = not led.value
