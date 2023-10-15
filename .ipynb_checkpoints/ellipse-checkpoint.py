import numpy as np
import matplotlib.pyplot as plt
import fullcontrol as fc
import create_gcode as cg

# Define parameters
A_sin = 6  # Amplitude of the sine wave
B_sin = 50    # Frequency of the sine wave
a = 50   # Semi-major axis 1
b = 50/2  # Semi-minor axis 1
phase_shift_sin = 17

A_cos = 6  # Amplitude of the cosine wave
B_cos = 50    # Frequency of the cosine wave
a_cos = 50 # Semi-major axis 2
b_cos = 50/2  # Semi-minor axis 2
phase_shift_cos = 0
h = 110    # x-coordinate of the center
k = 110  # y-coordinate of the center

z_height = 2
z_increment = 2.6
num_layers = 10

# Define the parametric equations
def r_sin(theta):
    return a * b / np.sqrt((b * np.cos(theta))**2 + (a * np.sin(theta))**2) + A_sin * np.sin(B_sin * theta + phase_shift_sin)

def r_cos(theta):
    return a_cos * b_cos / np.sqrt((b_cos * np.cos(theta))**2 + (a_cos * np.sin(theta))**2) + A_cos * np.cos(B_cos * theta + phase_shift_cos)

def x(theta, r):
    return h + r * np.cos(theta)

def y(theta, r):
    return k + r * np.sin(theta)

# Generate theta values
theta = np.linspace(0, 2*np.pi, 1000)

# Calculate r values for sine and cosine waves
r_values_sin = r_sin(theta)
r_values_cos = r_cos(theta)

# Calculate x and y for sine and cosine waves
x_values_sin = x(theta, r_values_sin)
y_values_sin = y(theta, r_values_sin)

x_values_cos = x(theta, r_values_cos)
y_values_cos = y(theta, r_values_cos)

z_values_sin = 1

steps = []

steps.extend(fc.travel_to(fc.Point(x=0, y=0,z=50)))
steps.extend(fc.travel_to(fc.Point(x=x_values_sin[1], y=y_values_sin[1],z=z_height+20)))

for i in range (0,num_layers):

    for i in range (0, len(x_values_sin)):
        xval = x_values_sin[i]
        yval = y_values_sin[i]
        steps.append(fc.Point(x=xval,y=yval,z=z_height))

    for i in range (0, len(x_values_cos)):
        xval = x_values_cos[i]
        yval = y_values_cos[i] 
        zval = z_values_sin
        steps.append(fc.Point(x=xval,y=yval,z=z_height))

    z_height = z_height + z_increment 

cg.custom_plot(steps)
gcode=cg.create_gcode(steps,'Oval')
fc.transform(steps,'sup')

# Plot the curves
# plt.figure(figsize=(8, 8))
# Plot sine wave
# plt.plot(x_values_sin, y_values_sin, label='Sine Wave', color='blue')
# Plot cosine wave
# plt.plot(x_values_cos, y_values_cos, label='Cosine Wave', color='red')
# plt.title("Ellipse with Sine and Cosine Wave Contours")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.axis('equal')
# plt.grid(True)
# plt.legend()
# plt.show()