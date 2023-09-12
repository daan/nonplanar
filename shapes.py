import fullcontrol as fc
import create_gcode as cg
import math
import lab.fullcontrol as fclab

def polygon():
    centre_point = fc.Point(x=220/3, y=220/3, z=3.5)
    enclosing_radius = 32
    start_angle = 0
    sides = 30
    clockwise = False
    steps = []
    # steps = fc.polygonXY(centre_point, enclosing_radius, start_angle, sides, clockwise)
    # steps.extend(fc.travel_to(fc.Point(x=73.3, y=73.7, z=2.5)))
    # steps.append(fc.Extruder(on=True))
    # steps.extend(fc.polygonXY(fc.Point(x=73.3, y=73.7, z=2.5), enclosing_radius, start_angle, sides, clockwise))
    # steps = fc.move(steps, fc.Vector(z=0.2), copy=True, copy_quantity=5)
    steps.extend(fc.polygonXY(fc.Point(x=73.3, y=146.6, z=2.5), enclosing_radius, start_angle, sides, clockwise))
    steps = fc.move(steps, fc.Vector(z=1), copy=True, copy_quantity=5)
    # steps.extend(fc.polygonXY(fc.Point(x=146.6, y=73.3, z=3.5), enclosing_radius, start_angle, sides, clockwise))
    # steps = fc.move(steps, fc.Vector(z=0.2), copy=True, copy_quantity=5)
    # steps.extend(fc.polygonXY(fc.Point(x=146.6, y=146.6, z=4), enclosing_radius, start_angle, sides, clockwise))
    # steps = fc.move(steps, fc.Vector(z=0.2), copy=True, copy_quantity=5)
    fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

    cg.custom_plot(steps)
    gcode = cg.create_gcode(steps,'Polygon(10)')
    # gcode_final = cg.split_gcode(gcode_raw)
    return(gcode)

def line_grid(): # Prints different lines (3 x 10) with varying height and changing flowrate (Better done with fclab.offset_path)
    steps = []; flow_rate = 2000; multiplier = 2; rows = 3; columns = 10; start_height = 0.2
    max_x = 220; max_y = 220; start_x = 20; start_y = 20; delta_x = 20        # X distance between the different lines
    delta_y = 10; line_lenght = 60; wait_time = 3; previous_z = 0; xdir = -1

    def wait (time):
        steps.append(fc.ManualGcode(text = "G4 P{}".format(wait_time*1000)))
        return

    for i in range (0, rows): # Number of rows
        # print('Moving to next row')
        steps.append(fc.ManualGcode(text = "M221 S{}".format(flow_rate)))
        start_height = 0.2 # Start of the fibonacci sequence
        previous_z = 0
        xdir = xdir *-1
        flow_rate = flow_rate  + 2000 # The increase in flowrate when switching to new row
        if i == 0:
            start_y = start_y
        else:
            start_y = start_y + line_lenght+ delta_y
        for j in range (0, columns): # Number of columns                 
            # print('Iteration number = ', j)
            steps.append(fc.Extruder(on=False))
            # print("Moving to start position :", start_x, start_y, '0')
            steps.append(fc.Point(x=start_x, y=start_y, z=0))
            wait(wait_time)
            steps.append(fc.Point(x=start_x, y=start_y, z=start_height))
            steps.append(fc.Extruder(on=True))
            test = start_y + line_lenght
            # print("Moving to destination :", start_x, start_y + line_lenght)
            steps.append(fc.Point(x=start_x, y=start_y + line_lenght, z=start_height))
            wait(wait_time)
            previous_z, start_height = start_height, previous_z + start_height
            # print("The new start height = ", start_height)
            start_x = start_x + (delta_x*xdir)
            if start_x == 220:
                start_x = 200

    cg.custom_plot(steps)
    gcode = cg.create_gcode(steps,'hello') #Retreives GCODE
    plot_controls = fc.PlotControls(raw_data=True)
    fc.transform(steps, 'plot2', fc.PlotControls(color_type='print_sequence', style='line'))
    return (gcode)

def polygon_sin(): # Prints a 2 layer circle with varying z-height sine wave
    steps = []; steps2 = []; start_height = 4.2; radius = 40; start_angle = 0; sides = 1000; clockwise = True; period = 0.10; num_layers = 2; amplitude = 1;
    centre_point = fc.Point(x=146,y=146,z=start_height)
    steps.extend(fc.polygonXY(centre_point,radius,start_angle,sides,clockwise))
    xval, yval, zval = cg.raw_data_xyz(steps)
    for j in range(0,num_layers):
        for i in range(0,len(xval)):
            zval_new = amplitude*math.sin(period*i)+zval[i]
            steps2.append(fc.Point(x=xval[i],y=yval[i],z=zval_new))
        period = 0.20

    cg.custom_plot(steps2)
    gcode = cg.create_gcode(steps2, 'poly_sin')
    print(gcode)

def single_line (start_point, end_point, back_forth):
    steps = []
    steps.extend(fc.travel_to(start_point))
    steps.append(start_point)
    steps.append(end_point)
    if back_forth == True:
      steps.append(end_point)  
      steps.append(start_point)  

    gcode = cg.create_gcode(steps,'single_line')
    cg.custom_plot(steps)
    return(gcode)

def polygon_cossin():
    steps = []; steps2 = []; start_height = 4.2; radius = 40; start_angle = 0; sides = 1000; clockwise = True; period = 0.10; num_layers = 2; amplitude = 5;
    centre_point = fc.Point(x=146,y=146,z=start_height)
    steps.extend(fc.polygonXY(centre_point,radius,start_angle,sides,clockwise))
    xval, yval, zval = cg.raw_data_xyz(steps)

    for j in range(0,num_layers+1):
        state = j % 2
        print('current state = ', state)
        if state == 1:
            for i in range(0,len(xval)):
                xval_sin = amplitude*math.sin(period*i)+xval[i]
                yval_sin = amplitude*math.sin(period*i)+yval[i]
                steps2.append(fc.Point(x=xval_sin,y=yval_sin,z=zval[i]))
        elif state == 0:
            for i in range(0,len(xval)):
                xval_cos = amplitude*math.cos(period*i)+xval[i]
                yval_cos = amplitude*math.cos(period*i)+yval[i]
                steps2.append(fc.Point(x=xval_cos,y=yval_cos,z=zval[i]))

    cg.custom_plot(steps2)
    gcode = cg.create_gcode(steps2, 'poly_sin')
    print(gcode)

def line_wave(state):
    z_height = 4.2
    start_point = fc.Point(x=20, y=10, z=z_height)
    direction = fc.Vector(x=0,y=1)
    amplitude = 5
    line_spacing = 10
    periods = 10
    steps = []
    
    if state == 1: # Squarewave
        line_spacing = 10
        periods = 10
        amplitude = 5
        print('line lenght = ',(line_spacing*2)*periods)
        start_point = fc.Point(x=150.5, y=15, z=4.2)
        start_point2 = fc.Point(x=150, y=210, z=4.2)
        direction_polar = 0.25 * math.tau
        direction_polar2 = 0.75 * math.tau
        steps.extend(fc.travel_to(start_point))
        steps.extend(fc.squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods)) #extra_half_period, extra_end_line
        steps.extend(fc.travel_to(start_point2))
        steps.extend(fc.squarewaveXYpolar(start_point2, direction_polar2, amplitude, line_spacing, periods)) #extra_half_period, extra_end_line
        fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))
        return cg.create_gcode(steps,'square_weave')
    

    if state == 2:  # Trianglewave
        # wave 5
        delta_x = 1.5
        start_point = fc.Point(x=120, y=15, z=4.2)
        start_point2 = fc.Point(x=120-delta_x, y=210, z=4.2)
        direction_polar = 0.25 * math.tau
        direction_polar2 = 0.75 * math.tau
        tip_separation = 5
        amplitude = 2
        periods = 40
        extra_half_period = False
        # steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
        steps.extend(fc.travel_to(start_point))
        steps.extend(fc.trianglewaveXYpolar(start_point, direction_polar, amplitude, tip_separation, periods, extra_half_period))
        steps.extend(fc.travel_to(start_point2))
        steps.extend(fc.trianglewaveXYpolar(start_point2, direction_polar2, amplitude, tip_separation, periods, extra_half_period)) #extra_half_period, extra_end_line
        fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))
        return cg.create_gcode(steps,'triangle_weave')
    

    if state == 3:  # Sinewave
        # wave 5
        delta_x = 3
        start_point = fc.Point(x=75, y=15, z=4.2)
        start_point2 = fc.Point(x=75-delta_x, y=215, z=4.2)
        direction_polar = 0.25 * math.tau
        direction_polar2 = 0.75 * math.tau
        amplitude = 3
        period_lenth = 10
        periods = 20
        segments_per_period = 16
        extra_half_period = False
        phase_shift = 0
        #   steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
        steps.extend(fc.travel_to(start_point))
        steps.extend(fc.sinewaveXYpolar(start_point, direction_polar, amplitude, period_lenth, periods, segments_per_period, extra_half_period, phase_shift))
        steps.extend(fc.sinewaveXYpolar(start_point2, direction_polar2, amplitude, period_lenth, periods, segments_per_period, extra_half_period, phase_shift))
        fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))
        return cg.create_gcode(steps,'sine_weave')
    
    fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

# line_wave(2)

# single_line(fc.Point(x=80, y=10, z=4.2), fc.Point(x=80, y=210, z=4.2), False)

line_wave(3)
# line_wave(2)