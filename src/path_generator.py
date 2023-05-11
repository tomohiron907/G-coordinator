import sys
import numpy as np
import math
#from print_settings import *
import print_settings
import matplotlib.pyplot as plt
from matplotlib.path import Path as matlabPath


class Path:
    def __init__(self, x=0, y=0, z=0):
        self.type = 'print'
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self.coords_arrange()
        self.set_print_settings()
        self.e_calc()
        
    def coords_arrange(self):
        self.coords = np.column_stack([self.x, self.y, self.z])
        self.center = np.array([np.mean(self.x), np.mean(self.y), np.mean(self.z)])
        self.start_coord = self.coords[0]
        self.end_coord = self.coords[-1]
        return self.coords
    
    def set_print_settings(self):
        self.array_number = len(self.x)
        self.extrusion_multiplier = None
        self.extrusion_multiplier_array = np.full(self.array_number, None)
        self.print_speed = None
        self.print_speed_array = np.full(self.array_number, None)
        self.retraction = None
        self.z_hop = None
        self.before_gcode = None
        self.after_gcode = None

    def e_calc(self):
        self.Eval = np.array([0])
        for i in range(len(self.coords)-1):
            Dis = math.sqrt((self.x[i+1]-self.x[i])**2 + (self.y[i+1]-self.y[i])**2 + (self.z[i+1]-self.z[i])**2)
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            self.Eval = np.append(self.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))


class PathList:
    def __init__(self, paths):
        self.paths = paths
        self._extrusion_multiplier = None
        self._print_speed = None
        self._retraction = None
        self._z_hop = None
        self._before_gcode = None
        self._after_gcode = None
        self.sort_paths()

    @property
    def extrusion_multiplier(self):
        return self._extrusion_multiplier

    @extrusion_multiplier.setter
    def extrusion_multiplier(self, value):
        self._extrusion_multiplier = value
        self._apply_print_settings()

    @property
    def print_speed(self):
        return self._print_speed

    @print_speed.setter
    def print_speed(self, value):
        self._print_speed = value
        self._apply_print_settings()

    @property
    def retraction(self):
        return self._retraction

    @retraction.setter
    def retraction(self, value):
        self._retraction = value
        self._apply_print_settings()

    @property
    def z_hop(self):
        return self._z_hop

    @z_hop.setter
    def z_hop(self, value):
        self._z_hop = value
        self._apply_print_settings()

    @property
    def before_gcode(self):
        return self._before_gcode

    @before_gcode.setter
    def before_gcode(self, value):
        self._before_gcode = value
        self._apply_print_settings()

    @property
    def after_gcode(self):
        return self._after_gcode

    @after_gcode.setter
    def after_gcode(self, value):
        self._after_gcode = value
        self._apply_print_settings()

    def _apply_print_settings(self):
        for path in self.paths:
            path.extrusion_multiplier = self.extrusion_multiplier
            path.print_speed = self.print_speed
            path.retraction = self.retraction
            path.z_hop = self.z_hop
            path.before_gcode = self.before_gcode
            path.after_gcode = self.after_gcode

    def sort_paths(self):
        sorted_paths = []
        remaining_paths = self.paths.copy()

        # 最初のパスを取り出し、ソート済みリストに追加
        current_path = remaining_paths.pop(0)
        sorted_paths.append(current_path)

        while remaining_paths:
            nearest_index = None
            min_distance = float('inf')

            # ソートされていないパスの中から最も近い始点を持つパスを探す
            for i, path in enumerate(remaining_paths):
                distance = np.linalg.norm(current_path.end_coord - path.start_coord)
                if distance < min_distance:
                    min_distance = distance
                    nearest_index = i

            # 最も近いパスを取り出し、ソート済みリストに追加
            current_path = remaining_paths.pop(nearest_index)
            sorted_paths.append(current_path)

        self.paths = sorted_paths
    
    


def flatten_path_list(full_object):
    flattened_paths = []
    for item in full_object:
        if isinstance(item, PathList):
            flattened_paths.extend(flatten_path_list(item.paths))
        elif isinstance(item, Path):
            flattened_paths.append(item)
    return flattened_paths


class Transform:
    def __init__(self):
        pass
    
    @staticmethod
    def twice_x(path):
        output_path = Path()
        output_path.x = 2 * path.x
        output_path.y = path.y
        output_path.z = path.z
        output_path.coords_arrange()
        return  output_path
        
    @staticmethod
    def rotate(path, theta):
        x = np.cos(theta)*path.x + np.sin(theta)*path.y
        y = -np.sin(theta)*path.x + np.cos(theta)*path.y
        z = path.z
        rotated_path = Path(x, y, z)
        return  rotated_path
        
    @staticmethod
    def offset(path, d):
        # Generate the offset polygon by computing the normal vectors of each vertex
        # and moving each vertex along its normal vector by the distance d
        polygon = path.coords
        offset_polygon = np.array([])
        offset_point_x = []
        offset_point_y = []
        offset_point_z = []
            
        for i in range( len(polygon)):
            # Compute the normal vector of the current vertex
            if np.allclose(polygon[0] , polygon[-1]):
                # 閉曲線
                p1 = polygon[(i-1)%(len(polygon)-1)]
                p2 = polygon[i%(len(polygon)-1)]
                p3 = polygon[(i+1)%(len(polygon)-1)]
            else:
                # 開曲線
                if i == 0:
                    # 開曲線の始点の処理
                    p1 = 2 * polygon[i] - polygon[i+1]
                    p2 = polygon[i]
                    p3 = polygon[i+1]
                elif i == len(polygon)-1:
                    # 開曲線の終点
                    p1 = polygon[i-1]
                    p2 = polygon[i]
                    p3 = 2 * polygon[i] - polygon[i-1]
                else:
                    # 開曲線の中間点
                    p1 = polygon[i-1]
                    p2 = polygon[i]
                    p3 = polygon[i+1]
            v1 = np.array([p2[0]-p1[0], p2[1]-p1[1]])
            v2 = np.array([p3[0]-p2[0], p3[1]-p2[1]])
            n = np.array([v1[1], -v1[0]])
            m = np.array([v2[1], -v2[0]])
            n /= np.linalg.norm(n)
            m /= np.linalg.norm(m)
            if np.dot(n, m) > 1:
                n_dot_m = 1
            elif np.dot(n, m) < -1:
                n_dot_m = -1
            else:
                n_dot_m = np.dot(n, m)
            phi = np.arccos(n_dot_m)
            theta = 2 * np.pi - phi - np.pi
            l = d / np.sin(theta /2)


            normal = n + m
            normal /= np.linalg.norm(normal)
            # Move the current vertex along its normal vector by the distance l
            offset_point = np.array([p2[0], p2[1]]) + l*normal
            offset_point_x.append(offset_point[0])
            offset_point_y.append(offset_point[1])
            offset_point_z.append(polygon[i, 2])
        

        offset_path = Path(offset_point_x, offset_point_y, offset_point_z)
        return offset_path

    @staticmethod
    def fill(path, infill_distance = 0.4, angle = np.pi/4, offset = 0):
        path = Transform.offset(path, offset)
        x = path.x
        y = path.y
        if angle == np.pi/2 or angle == -np.pi/2:
            angle -=0.001
        y_intersept = infill_distance / math.cos(angle)
        K = np.arange(-200/math.cos(angle),200/math.cos(angle),y_intersept)
        Xlist=[]
        Ylist=[]
        
        
        slope = math.tan(angle)
        for k in K:
            for n in range(len(path.coords)-1):
                if (slope*x[n+1] - y[n+1] + k )* (slope*x[n] - y [n] +k) < 0:
                    X=(x[n+1]*y[n]-y[n+1]*x[n]-(x[n+1]-x[n])*k)/(slope*(x[n+1]-x[n])-(y[n+1]-y[n]))
                    Y=slope*X+k
                    Xlist.append(X)
                    Ylist.append(Y)
                

        for i in range(len(Xlist)-1):
            if i%4==2:
                Xlist[i],Xlist[i+1]=Xlist[i+1],Xlist[i]
                Ylist[i],Ylist[i+1]=Ylist[i+1],Ylist[i]
                
                
        for i in range(len(Xlist)-1):
            if i%2==0:
                if (slope*Xlist[i]-Ylist[i])<(slope*x[0]-y[0]):
                    Xlist[i],Xlist[i+1]=Xlist[i+1],Xlist[i]
                    Ylist[i],Ylist[i+1]=Ylist[i+1],Ylist[i]
        Zlist = [path.z[0] for i in range(len(Xlist))]


        filled_path = Path(Xlist, Ylist, Zlist)
        return filled_path



def gyroid_infill(path, z_height, resolution = 40, d = 1/2, value = 0):
    x_list = path.x
    y_list = path.y
    # Grid parameters
      # Resolution of the grid
    x = np.linspace(np.min(x_list), np.max(x_list), resolution)
    y = np.linspace(np.min(y_list), np.max(y_list), resolution)
    X, Y = np.meshgrid(x, y)
    
    # Equation for the Gyroid surface
    theta = 0
    #equation = np.sin(X/d) * np.cos(Y/d) + np.sin(Y/d) * np.cos(z_height) + np.sin(z_height) * np.cos(X/d)
    equation = np.sin(X/d*np.cos(theta) + Y/d*np.sin(theta)) * np.cos(-X/d*np.sin(theta) + Y/d*np.cos(theta)) + np.sin(-X/d*np.sin(theta) + Y/d*np.cos(theta)) * np.cos(z_height/d) + np.sin(z_height/d) * np.cos(X/d*np.cos(theta) + Y/d*np.sin(theta))-value

    # Determine the inside region
    inside = np.ones_like(equation)
    path = matlabPath(np.column_stack([x_list, y_list]))

    points = np.column_stack((X.flatten(), Y.flatten()))
    inside = path.contains_points(points)
    inside = inside.reshape(X.shape).astype(float)
    inside[inside == 0] = np.nan

    # Plot the slices
    slice_plane = equation * inside
    contours = plt.contour(x, y, slice_plane, levels=[0], colors='black')

    infill_path_list = []
    for contour in contours.collections:
            paths = contour.get_paths()
            for path in paths:
                points = path.vertices
                x_coords = points[:, 0]
                y_coords = points[:, 1]
                z_coords = np.full_like(x_coords, z_height)
                wall = Path(x_coords, y_coords, z_coords)
                infill_path_list.append(wall)
    return PathList(infill_path_list)

