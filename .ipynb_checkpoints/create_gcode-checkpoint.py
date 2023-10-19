import fullcontrol as fc
import plotly.graph_objects as go
import numpy as np
import json
import re

def create_gcode(printer_steps, fileName): #Creates gcode of fullcontrol steps and saves it. Printer parameters can be adjusted here
    nozzle_temp = 220
    bed_temp = 20
    print_speed = 300  # 300 = 5 mm/s & 6000 = 100 mm/s
    fan_percent = 0
    flow_rate = 2000
    printer_name='ender_3' # ultimaker2plus
    EW = 0.8# extrusion width # 0.4
    EH = 0.2 # extrusion height (and layer height) #0.2

    folder_name = 'created gcode'    # Define the folder name
    file_path = f'{folder_name}/{fileName}.gcode'   # Combine the folder and file names

    gcode_controls = fc.GcodeControls(
    printer_name=printer_name,

    initialization_data={
       'primer': 'no_primer',
        'print_speed': print_speed,
        'nozzle_temp': nozzle_temp,
        'material_flow_percent': flow_rate,
        'bed_temp': bed_temp,
        'fan_percent': fan_percent,
        'extrusion_width': EW,
        'extrusion_height': EH})
    gcode_fc = fc.transform(printer_steps, 'gcode', gcode_controls)
    open(file_path, 'w').write(gcode_fc)  #This file is suitable for printing with SD card
    
    # gcode = []
    # gcode_serial = gcode_fc.split('\n')
    # for seperate_lines in gcode_serial:
    #     if "M105" in seperate_lines: #M105 Seems to stall serial communication for me
    #         continue
    #     else:
    #         gcode.append(seperate_lines)
    # return (gcode) #This code can be send through serial communication

def custom_plot(plot_data): # Returns a custom plot of the fullcontrol steps (I use it as an alternative for the fc.Transform function, which often does not work)
    raw_plot = fc.PlotControls(raw_data=True)
    data=fc.transform(plot_data,'plot', raw_plot)
    fig = go.Figure(layout=go.Layout(template='plotly_white'))

    fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=4, range=[0,220],),
                     yaxis = dict(nticks=4, range=[0,220],),
                     zaxis = dict(nticks=4, range=[0,220],),),
    width=1400,
    margin=dict(r=20, l=10, b=10, t=10))

    for i in range(len(data.paths)):
        line_color = 'rgb(255,160,0)' if data.paths[i].extruder.on == True else 'rgb(200,0,0)'
        fig.add_trace(go.Scatter3d(mode='lines', x=data.paths[i].xvals, y=data.paths[i].yvals,z=data.paths[i].zvals, line=dict(color=line_color)))
    
    fig.show()

def raw_data(data): # Returns grouped XYZ data of the fullcontrol steps
    raw_plot = fc.PlotControls(raw_data=True)
    raw_data=fc.transform(data,'plot', raw_plot)
    return(raw_data)

def raw_data_xyz(data): # Returns raw X, Y, Z data of the fullcontrol steps
    raw_plot = fc.PlotControls(raw_data=True)
    raw_data=fc.transform(data,'plot', raw_plot)
    xval = (f'{raw_data.paths[0].xvals}')
    yval = (f'{raw_data.paths[0].yvals}')
    zval = (f'{raw_data.paths[0].zvals}') 

    x_array = json.loads(xval)
    y_array = json.loads(yval)
    z_array = json.loads(zval)
    return(x_array, y_array, z_array)

def extract_steps(file_path): #Extract fullcontrol XY steps from an existing gcode file (usefull for DXF files)
    # Specify the path to your G-code file

    # Initialize empty lists to store X and Y coordinates
    x_coordinates = []
    y_coordinates = []

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        gcode = file.read()

        # Split the G-code into lines and iterate through them
        for line in gcode.split('\n'):
            if 'G1' in line:
                match = re.search(r'X([\d.]+)\s+Y([\d.]+)', line)
                if match:
                    x_coordinates.append(float(match.group(1)))
                    y_coordinates.append(float(match.group(2)))

    # Print the coordinates
    # print("X Coordinates:", x_coordinates)
    # print("Y Coordinates:", y_coordinates)
    return x_coordinates, y_coordinates

def adjust_z_height(gcode_line, new_z):
    match = re.match(r'(G[01])?(?:\s*F(\d+))?(?:\s*X([\d.-]+))?(?:\s*Y([\d.-]+))?(?:\s*Z([\d.-]+))?(?:\s*E([\d.-]+))?', gcode_line)
    if match:
        command = match.group(1)
        feed_rate = int(match.group(2)) if match.group(2) else None
        x_value = float(match.group(3)) if match.group(3) else None
        y_value = float(match.group(4)) if match.group(4) else None
        z_value = float(match.group(5)) if match.group(5) else None
        e_value = float(match.group(6)) if match.group(6) else None

        new_line = ""
        if command is not None:
            new_line += f'{command}'
        if feed_rate is not None:
            new_line += f' F{feed_rate}'
        if x_value is not None:
            new_line += f' X{x_value}'
        if y_value is not None:
            new_line += f' Y{y_value}'
        if new_z is not None:
            new_line += f' Z{new_z}'
        if e_value is not None:
            new_line += f' E{e_value}'
        
        # print(new_line)
        return new_line
    else:
        print(f"Could not parse line: {gcode_line}")
        return None

def extract_stepsXYZ(file_path): 
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []

    with open(file_path, 'r') as file:
        gcode = file.read()

        for line in gcode.split('\n'):
            if 'G1' in line:
                matches = re.finditer(r'X([\d.]+)\s+Y([\d.]+)(?:\s+X([\d.]+))?\s+Z([\d.]+)?', line)
                for match in matches:
                    x_coordinates.append(float(match.group(1)))
                    y_coordinates.append(float(match.group(2)))
                    z_coordinates.append(float(match.group(4)) if match.group(4) is not None else None)

    # print("X Coordinates:", x_coordinates)
    # print("Y Coordinates:", y_coordinates)
    # print("Z Coordinates:", z_coordinates)

    return x_coordinates, y_coordinates, z_coordinates