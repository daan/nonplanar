import time
import sys
import serial
from enumerate_serial_ports import *
import math


class SerialDevice:
    def __init__(self):
        self._response = ""

    def open(self, p):
        print("opening port {}".format(p))
        try:
            self.ser = serial.Serial(port=p, baudrate=250000, timeout=0, xonxoff=False)
        except:
            print("Error opening serial port {}".format(p))
            sys.exit()
        self.handle_response()

    def close(self):
        self.ser.close()

    def handle_response(self):
        if self.ser.in_waiting != 0:
            c = self.ser.read()
            if c == b"\n":
                s = self._response
                self._response = ""
                return s
            else:
                self._response += c.decode("utf-8")


class Printer(SerialDevice):
    def home(self):
        self.send_gcode("G28")

    def move(self, x, y, z, speed=200):
        self.send_gcode(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f} F{speed}")

    def move_x(self, x, speed=200):
        gcode = "G01 X " + str(x) + "F" + str(speed)
        self.send_gcode(gcode)

    def move_y(self, y, speed=200):
        gcode = "G01 Y " + str(y) + "F" + str(speed)
        self.send_gcode(gcode)

    def move_z(self, z, speed=200):
        gcode = "G01 Z " + str(z) + "F" + str(speed)
        self.send_gcode(gcode)

    def send_gcode(self, gcode):
        gcode += "\n"
        print("sending gcode", gcode.encode())
        self.ser.write(gcode.encode())

    def wait_for_ok(self):
        while True:
            s = self.handle_response()
            if s != None:
                print(s)
                if s == "ok":
                    return


print("connecting to the last available serial port")
p = SerialDevice()
p.open(enumerate_serial_ports()[-1])

print("connecting to the printer")
p = Printer()
p.open(enumerate_serial_ports()[-2])
time.sleep(1.0)
while True:
    s = p.handle_response()
    if s == None:
        print("init done")
        break
    else:
        print(s)

p.home()
p.wait_for_ok()
p.move(100, 100, 50, speed=3000)
p.wait_for_ok()


while True:
    time.sleep(0.1)
    s = p.handle_response()
    if s == None:
        print(s)
