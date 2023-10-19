import board
import busio
import digitalio
import analogio
import time
import math

needs_homing = True


class gcode_reader:
    def __init__(self, filename):
        self._fp = open(filename, "r")
        self._filename = filename

    def readline(self):
        return self._fp.readline().strip()

    def reset(self):
        self._fp.close()
        self._fp = open(self._filename, "r")


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


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=115200)

init_reader = None
circle_reader = None


class State:
    start = 1
    is_homing = 10
    initialize = 20
    ready = 30


def start_initializing():
    global current_state
    global init_reader
    print("start initializing1")
    current_state = State.initialize
    init_reader = gcode_reader("init.gcode")
    line = init_reader.readline()
    print(line)
    write_line(line)


def start_ready():
    global current_state
    global circle_reader

    print("start ready")
    current_state = State.ready
    circle_reader = gcode_reader("circle.gcode")
    line = circle_reader.readline()
    print("***", line)
    write_line(line)


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
steps = 3600
c_zero = 0.0

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
        print(line)
        # print(current_state, line) #, f"\t{(time.monotonic() - c_last):.4f}")

        if line[0:2] == "ok":
            if current_state == State.ready:
                line = circle_reader.readline()
                if line == "":
                    circle_reader.reset()
                    line = circle_reader.readline()
                write_line(line)

                # i = (i + 1) % steps
                #
                # if i == 0:
                #    print(radius, steps, f"\t{(time.monotonic() - c_zero):.4f}")
                #    c_zero = time.monotonic()

                # x = 100 + radius * math.cos(math.pi * 2 * (i / steps))
                # y = 100 + radius * math.sin(math.pi * 2 * (i / steps))

                # target_pot_value = pot_value_in_mm()

                # if target_pot_value > current_z_value:
                #    current_z_value += 0.2
                # else:
                #    current_z_value -= 0.2
                #
                # z = 10+current_z_value / 12

                print(f"circle line : {line}")

                # write_line(f"G0 X{x:.2f} Y{y:.2f} F300") # Z{z:.2f}")

            if current_state == State.initialize:
                line = init_reader.readline()
                if line != "":
                    write_line(line)
                    print(f"init line : {line}")
                else:
                    print("ready")
                    start_ready()

            if current_state == State.is_homing:
                print("homing done")
                start_initializing()

    if current_state == State.start:
        if needs_homing:
            print("start homing")
            write_line("G28")
            current_state = State.is_homing

    # heartbeat
    t = time.monotonic()
    if t > t_last + 0.2:
        t_last = t
        led.value = not led.value
        # print(pot_value_in_mm())
