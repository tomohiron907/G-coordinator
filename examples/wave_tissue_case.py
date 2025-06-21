# Author: Yadanium (@yada_kaeru)

import numpy as np
import gcoordinator as gc

LAYER = 400
layer_hight = 0.5

#1.0mmノズルで計算した高さ
#1.0mmノズルの場合layer_hightは0.5
#原点（origin）x=50, y=50
#速度（speed）print_speed及びtravel_speedは1000
#リトラクション有り

#点と点の間をsin波で補間する
def create_sinusoidal_path(x_points, y_points, num_points=300, amplitude=2, phase_shift=0):
#amplitudeの値で厚みを変えられます
    
    result_x = []
    result_y = []
    
    for i in range(len(x_points)-1):
        x1, x2 = x_points[i], x_points[i+1]
        y1, y2 = y_points[i], y_points[i+1]
        
        # 2点間の距離を計算
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        # 距離に応じて波の数を調整（長い線分はより多くの波を持つ）
        num_waves = max(0, int(distance/6))
        
        t = np.linspace(0, 1, num_points)
        
        # 直線上の点を計算
        line_x = x1 + (x2 - x1) * t
        line_y = y1 + (y2 - y1) * t
        
        # 直線の角度を計算
        angle = np.arctan2(y2 - y1, x2 - x1)
        
        # より細かいsin波を適用
        dx = amplitude * np.sin(2 * np.pi * num_waves * t + phase_shift) * np.sin(angle)
        dy = -amplitude * np.sin(2 * np.pi * num_waves * t + phase_shift) * np.cos(angle)
        
        result_x.extend(line_x + dx)
        result_y.extend(line_y + dy)
    
    return np.array(result_x), np.array(result_y)

full_object = []
for height in range(LAYER):
    x_orig = (50,50,48,48,0,0,106,106,58,58,56,56)
    y_orig = (62,67.5,67.5,64,64,0,0,64,64,67.5,67.5,62)
    
    # 偶数層と奇数層で位相をずらす
    phase = np.pi if height % 2 == 1 else 0
    x, y = create_sinusoidal_path(x_orig, y_orig, phase_shift=phase)
    z = np.full_like(x, (height+1)*layer_hight+1)
    
    wall = gc.Path(x, y, z)
    full_object.append(wall)

gc.gui_export(full_object)