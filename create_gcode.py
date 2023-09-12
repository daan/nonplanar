import fullcontrol as fc
import plotly.graph_objects as go
import numpy as np
import json

def create_gcode(printer_steps, fileName): #Creates gcode of fullcontrol steps and saves it. Adjust the variables 
    nozzle_temp = 220
    bed_temp = 20
    print_speed = 300  # 300 = 5 mm/s & 6000 = 100 mm/s
    fan_percent = 0
    flow_rate = 2000
    printer_name='ender_3' # ultimaker2plus
    EW = 0.8# extrusion width # 0.4
    EH = 0.2 # extrusion height (and layer height) #0.2

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
    open(f'{fileName}.gcode', 'w').write(gcode_fc) #This file is suitable for printing with SD card
    
    gcode = []
    gcode_serial = gcode_fc.split('\n')
    for seperate_lines in gcode_serial:
        if "M105" in seperate_lines: #M105 Seems to stall serial communication for me
            continue
        else:
            gcode.append(seperate_lines)
    return (gcode) #This code can be send through serial communication

def custom_plot(plot_data): # Returns a custom plot of the fullcontrol steps (I use it as an alternative for the fc.Transform function)
    raw_plot = fc.PlotControls(raw_data=True)
    data=fc.transform(plot_data,'plot', raw_plot)
    fig = go.Figure(layout=go.Layout(template='plotly_dark'))

    for i in range(len(data.paths)):
        line_color = 'rgb(255,160,0)' if data.paths[i].extruder.on == True else 'rgb(200,0,0)'
        fig.add_trace(go.Scatter3d(mode='lines', x=data.paths[i].xvals, y=data.paths[i].yvals,z=data.paths[i].zvals, line=dict(color=line_color)))

    fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=4, range=[0,220],),
                     yaxis = dict(nticks=4, range=[0,220],),
                     zaxis = dict(nticks=4, range=[0,100],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))

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


