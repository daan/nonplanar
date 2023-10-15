import board
import busio
import digitalio
import time
import math

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

t_last = time.monotonic()
# uart = busio.UART(board.D10, board.D11, baudrate=250000)
uart = busio.UART(board.TX, board.RX, baudrate=115200)

homed = False

incoming_line = ""

def read_line():
    global incoming_line
    while True:
        c = uart.read(1)
        if c is None:
            return None
        if c == b'\n':
            line = incoming_line
            incoming_line = ""
            return line
        incoming_line += c.decode("utf-8")

def write_line(gcode):
    uart.write(bytes(gcode + "\n", "ascii"))

i = 0
radius = 10

while True:
    i = (i+1) % 360
    x = 100 + radius * math.cos(math.radians(i))
    y = 100 + radius * math.sin(math.radians(i))
    
    line = read_line()
    if line is not None:
        if line == "ok":
            write_line(f"G0 X{x:.2f} Y{y:.2f}")

    t = time.monotonic()
    # heartbeat
    if t > t_last + 1.0:
        t_last = t
        led.value = not led.value
        if not homed:
            uart.write(bytes("G28\n", "ascii"))
            uart.write(bytes("G0 X100 Y100 Z20 f10000\n", "ascii"))
            homed = True

