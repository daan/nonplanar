gcode_fp = None

print("start")


def open_gcode_file(s):
    global gcode_fp
    gcode_fp = open(s)


def read_gcode_line():
    global gcode_fp
    try:
        line = gcode_fp.readline().strip()
    except:
        print("file reading error")
    return line


open_gcode_file("Oval.gcode")

while 1:
    line = read_gcode_line()
    if line == "":
        break
    print(line)

print("done!")
