import numpy as np
import math
import print_settings 
from path_generator import *
from infill_generator import line_infill


#LAYER =300







x_coords = np.array([0])
y_coords = np.array([0])
def draw_koch_snowflake(order, length, angle, x, y):
    global x_coords, y_coords
    if order == 0:
        # ラインを描画
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        x_coords = np.append(x_coords, x_end)
        y_coords = np.append(y_coords, y_end)
        #plt.plot([x, x_end], [y, y_end], 'k')
    else:
        length /= 3.0
        draw_koch_snowflake(order - 1, length, angle, x, y)  # 1/3の位置まで再帰的に描画
        x = x + length * np.cos(np.radians(angle))
        y = y + length * np.sin(np.radians(angle))
        draw_koch_snowflake(order - 1, length, angle - 60, x, y)  # 60度左に曲がって再帰的に描画
        x = x + length * np.cos(np.radians(angle - 60))
        y = y + length * np.sin(np.radians(angle - 60))
        draw_koch_snowflake(order - 1, length, angle + 60, x, y)  # 60度右に曲がって再帰的に描画
        x = x + length * np.cos(np.radians(angle + 60))
        y = y + length * np.sin(np.radians(angle + 60))
        draw_koch_snowflake(order - 1, length, angle, x, y)  # 1/3の位置まで再帰的に描画



R = 60
LAYER = int(60 / 0.2 * np.sqrt(2)/2)

def object_modeling():
    global x_coords, y_coords
    full_object=[]
    for height in range(LAYER):
        x_coords = np.array([0])
        y_coords = np.array([0])
        
        a = np.sqrt(2) * height /LAYER * R - np.sqrt(2)/2*R
        
        initial_length =np.sqrt(R**2 - a**2)
        initial_angle = 0
        draw_koch_snowflake(4, initial_length, initial_angle, 0, 0)
        draw_koch_snowflake(4, initial_length, initial_angle + 120, initial_length, 0)
        draw_koch_snowflake(4, initial_length, initial_angle +240, initial_length/2, initial_length/2*np.sqrt(3))

        z = np.full_like(x_coords, height*0.2)
        wall = Path(x_coords, y_coords, z)
        wall = Transform.move(wall, -initial_length/2, -initial_length/2*np.sqrt(3)*1/3)
        wall = Transform.rotate(wall, -height/LAYER * np.pi/2)
        full_object.append(wall)
        '''outer_wall = Transform.offset(wall, -0.4)
        full_object.append(outer_wall)'''
        if height<3:
            infill = line_infill(wall, 0.98, height*np.pi/2 + np.pi/4)
            full_object.append(infill)
        


    return full_object
    

