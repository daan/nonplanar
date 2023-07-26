import sys
import glob
import serial
import serial.tools.list_ports

# USB_VENDOR_DICT

usbvid = {9114: "Adafruit", 10161: "Ultimachine"}


def print_ports():
    for p in serial.tools.list_ports.comports():
        vid = str(p.vid)
        if p.vid in usbvid:
            vid += f" {usbvid[p.vid]}"
        print(p)
        print(f"{p.device} vid:{vid} pid:{p.pid} {p.description}")


def enumerate_ports():
    return [p.device for p in serial.tools.list_ports.comports()]


def get_ports_with_vid(vid):
    return [p.device for p in serial.tools.list_ports.comports() if p.vid == vid]


# somewhat based on http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# TODO: i didn't test linux or macos yet, but it looks like the list_ports
# in pyserial does this also
def enumerate_serial_ports():
    if sys.platform.startswith("win"):
        ports = ["COM" + str(i + 1) for i in range(256)]
    elif sys.platform.startswith("linux"):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")

    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        if port == "/dev/tty.Bluetooth-Incoming-Port":
            continue
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == "__main__":
    print_ports()
    print(enumerate_ports())
    print(get_ports_with_vid(9114))
