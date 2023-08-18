import re

def extract_z_values(file_path):
    z_values = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file.readlines(), 1):
            match = re.search(r'Z(-?\d+\.?\d*)', line)
            if match:
                z_value = float(match.group(1))
                z_values.append((z_value, line_number))
    return z_values

def find_closest_z(target, z_values):
    closest_value, closest_line = None, None
    min_diff = float('inf')
    
    for value, line_number in z_values:
        diff = abs(target - value)
        if diff < min_diff:
            min_diff = diff
            closest_value = value
            closest_line = line_number
            
    return closest_value, closest_line

def extract_lines_between_z(file_path, start_line, z_values):
    lines_between = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file.readlines(), 1):
            if line_number > start_line:
                if re.search(r'Z(-?\d+\.?\d*)', line):
                    break
                lines_between.append(line.strip())
    return lines_between


file_path = 'CE3E3V2_Foot.gcode' #.gcode file
z_values = extract_z_values(file_path) #List of z heights
z_values = z_values[:-2] #Final homing code post print in the .gCode
target_z = float(input("Enter the target Z value: ")) #search a z layer
closest_value, closest_line = find_closest_z(target_z, z_values) #find the closest z value and what line it happens on


with open(file_path) as f:
    [print(line) for line in f.readlines()]

for value, line_number in z_values:
    print(f'Z value: {value} found on line {line_number}')

print(f'Closest Z value: {closest_value} found on line {closest_line}')

lines_between = extract_lines_between_z(file_path, closest_line, z_values) #Single Z layer of gCode. (multiple Z's in a layer will not work)
for line in lines_between:
    print(line)