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

ain1 = digitalio.DigitalInOut(board.D24)
ain1.direction = digitalio.Direction.OUTPUT
ain2 = digitalio.DigitalInOut(board.D25)
ain2.direction = digitalio.Direction.OUTPUT
apwm = pwmio.PWMOut(board.D2)
apwm.duty_cycle = 0


def set_target(v):
    target = v
    print(f"new target {v}")


def set_motor(speed):
    if speed < 0:
        ain1.value = True
        ain2.value = False
    else:
        ain1.value = False
        ain2.value = True
    apwm.duty_cycle = abs(speed)


# set_speed(65535)
# time.sleep(0.2)

# set_speed(-65535)
# time.sleep(0.2)

print("done")

# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
last_value = pot.value / 65535

t_last = time.monotonic()

target = 32535

while True:
    # data = uart.read(32)  # read up to 32 bytes
    # print(data)  # this is a bytearray type

    v = pot.value
    delta = abs(target - v)
    if delta > 200:
        if v < target:
            set_motor(65535)
        else:
            set_motor(-65535)
    else:
        set_motor(0)

    value = pot.value / 65535
    if fabs(last_value - value) > 0.02:
        print(f"{pot.value / 65535:.2f} {v} {target} {delta}")
        last_value = value
    t = time.monotonic()
    # heartbeat
    if t > t_last + 0.5:
        t_last = t
        led.value = not led.value
