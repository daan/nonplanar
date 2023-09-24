#
#   in circuit python. use MU editor
#   open serial.
#   type a float and hit enter in the serial window to move the motor
#   set debug_printing to False when testing with the host side script.

#
#   TODO: first read message seems ignored. not an issue, but yes.
#

debug_printing = False
def debug(str):
    if debug_printing:
        print(f"debug: {str}")
    
import board
import digitalio
import analogio
import pwmio
import busio
import touchio
import supervisor
import sys

import time
from math import fabs

# crap circuitpython no ticks_ms()
t_last = time.monotonic()

# heartbeat
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#
# pot meter
#
pot = analogio.AnalogIn(board.A0)
pot_length = 120.0  # in mm; starting at the motor.
# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
def pot_value_in_mm():
    return (pot.value / 65535.0) * pot_length
last_pot_value = pot_value_in_mm()

#
# touch pad
#

touch_pad = board.A1
touch = touchio.TouchIn(touch_pad)
# True when the knob is being touched.
last_touch_state = False

#
# motor
#

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

target = 60  # mm
buffer = ""

while True:
    # deal with touch
    if touch.value != last_touch_state:
        if last_touch_state:
            # user stopped touching
            target = pot_value_in_mm()
            last_touch_state = False
            debug(f"end touch {target:.2f}")
            print(f"{target:.2f}")
        else:
            last_touch_state = True
            debug("start touch")
    if touch.value:
        set_motor(0)  # no motor when user touches
    else:
        v = pot_value_in_mm()
        delta = abs(target - v)
        speed = 65535 # max speed
        if delta > 1:
            if v < target:
                set_motor(speed)
            else:
                set_motor(-speed)
            debug(f"move motor {v} {target}")
        else:
            set_motor(0)        
        
        
        
    # print the value when touching
    if touch.value:
        value = pot_value_in_mm()
        if fabs(last_pot_value - value) > 1:  # only print when changed > 1 mm
            debug(f"{pot_value_in_mm():.2f}")
            last_value = value
        
    # input from host pc        
    while supervisor.runtime.serial_bytes_available:
        c = sys.stdin.read(1)
        if c == "\n":
            try:
                target = min(pot_length-1.0, max(0.0, float(buffer))) # HACK: looks like 119 is max of the pot....
                debug(f"received target: {target}")                
            except (TypeError, ValueError):
                pass
            buffer = ""
        else:
            buffer += c

    # heartbeat, to show that the main loop is still running            
    t = time.monotonic()
    if t > t_last + 0.5:
        t_last = t
        led.value = not led.value
        