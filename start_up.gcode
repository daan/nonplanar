G28 ; home axes
M140 S20 ; set bed temp and continue
M105
M104 S220 ; set hotend temp and continue
M190 S20 ; set bed temp and wait
M105
M109 S220  ; set hotend temp and wait
G90 ; absolute coordinates
G21 ; set units to millimeters
M83 ; relative extrusion
M106 S0 ; set fan speed
M220 S100 ; set speed factor override percentage
M221 S2000 ; set extrude factor override percentage
G0 F8000 X5.0 Y5.0 Z10.0
G1 F250 E2.0
G0 F250 Z10.0
G0 F8000 X10.0 Y10.0 Z0.3
