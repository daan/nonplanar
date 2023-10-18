import board
import busio
import digitalio
import analogio
import time
import math
import rotaryio

needs_homing = True


#
# pot meter
#
pot = analogio.AnalogIn(board.A0)
pot_length = 120.0  # in mm; starting at the motor.


# rp2040 adc is 12 bit, but circuitpython presents it as 16bit
def pot_value_in_mm():
    return (pot.value / 65535.0) * pot_length


target_pot_value = pot_value_in_mm()
current_z_value = pot_value_in_mm()

#
#Rotary Encoders
#

flow_encoder = rotaryio.IncrementalEncoder(board.D10, board.D11)
last_flow_position = None
speed_encoder = rotaryio.IncrementalEncoder(board.D7, board.D9)
last_speed_position = None


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=115200)


class State:
    start = 1
    is_homing = 10
    initialize = 20
    ready = 30


current_state = State.start

incoming_line = ""
t_last = time.monotonic()


def read_line():
    global incoming_line
    while True:
        c = uart.read(1)
        if c is None:
            return None
        if c == b"\n":
            line = incoming_line
            incoming_line = ""
            return line
        incoming_line += c.decode("utf-8")


def write_line(gcode):
    uart.write(bytes(gcode + "\n", "ascii"))


i = 0
radius = 50
steps = 4000

c_last = 0.0


#
# always some junk in the buffer
#

write_line("M119")


while True:
    line = read_line()
    if line is not None:
        pass
    else:
        break

while True:
    line = read_line()
    if line is not None:
        print(current_state, line)  # , f"\t{(time.monotonic() - c_last):.4f}")

        if line[0:2] == "ok":
            if current_state == State.is_homing:
                print("homing done")
                current_state = State.initialize
            if current_state == State.initialize:
                print("ready")
                current_state = State.ready
            if current_state == State.ready:
                i = (i + 1) % steps
                x = 100 + radius * math.cos(math.pi * 2 * (i / steps))
                y = 100 + radius * math.sin(math.pi * 2 * (i / steps))

                target_pot_value = pot_value_in_mm()

                if target_pot_value > current_z_value:
                    current_z_value += 0.2
                else:
                    current_z_value -= 0.2

                z = 10 + current_z_value / 12

                e = 0.5

                f = 300

                write_line(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} E {z:.2f} F{z:.2f}")
                c_last = time.monotonic()

    if current_state == State.start:
        if needs_homing:
            write_line("M104 S220") 
            print("start homing")
            write_line("G28")
            current_state = State.is_homing
        else:
            current_state = State.initialize

    if current_state == State.initialize:
        print("init sequence")
        write_line("G0 X100 Y100 Z20 f10000")
        write_line("M83") 
        write_line("M109 S220") 

    # heartbeat
    t = time.monotonic()
    if t > t_last + 0.2:
        t_last = t
        led.value = not led.value
        print(pot_value_in_mm())
