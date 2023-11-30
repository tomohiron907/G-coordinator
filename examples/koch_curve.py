import numpy as np
import gcoordinator as gc

x_coords = np.array([0])
y_coords = np.array([0])
def draw_koch_snowflake(order, length, angle, x, y):
    global x_coords, y_coords
    if order == 0:
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        x_coords = np.append(x_coords, x_end)
        y_coords = np.append(y_coords, y_end)
    else:
        length /= 3.0
        draw_koch_snowflake(order - 1, length, angle, x, y)  
        x = x + length * np.cos(np.radians(angle))
        y = y + length * np.sin(np.radians(angle))
        draw_koch_snowflake(order - 1, length, angle - 60, x, y)  
        x = x + length * np.cos(np.radians(angle - 60))
        y = y + length * np.sin(np.radians(angle - 60))
        draw_koch_snowflake(order - 1, length, angle + 60, x, y)  
        x = x + length * np.cos(np.radians(angle + 60))
        y = y + length * np.sin(np.radians(angle + 60))
        draw_koch_snowflake(order - 1, length, angle, x, y)



R = 150
arg = np.pi/5
LAYER = int(R / 0.2 * np.cos(arg))


full_object=[]
for height in range(LAYER):
    x_coords = np.array([0])
    y_coords = np.array([0])
    
    a = np.cos(arg)*2 * height /LAYER * R - np.cos(arg)*R
    
    initial_length =np.sqrt(R**2 - a**2)
    initial_angle = 0
    draw_koch_snowflake(4, initial_length, initial_angle, 0, 0)
    draw_koch_snowflake(4, initial_length, initial_angle + 120, initial_length, 0)
    draw_koch_snowflake(4, initial_length, initial_angle +240, initial_length/2, initial_length/2*np.sqrt(3))

    z = np.full_like(x_coords, height*0.2 + 0.2)
    wall = gc.Path(x_coords, y_coords, z)
    wall = gc.Transform.move(wall, -initial_length/2, -initial_length/2*np.sqrt(3)*1/3)
    wall = gc.Transform.rotate_xy(wall, -height/LAYER * np.pi/2)
    full_object.append(wall)

    if height<3:
        infill = gc.line_infill(wall, infill_distance = 1, angle=height*np.pi/2 + np.pi/4)
        infill.z_hop = True
        infill.retraction = True
        full_object.append(infill)
    
gc.gui_export(full_object)
    

