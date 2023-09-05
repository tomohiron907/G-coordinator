import sys
import numpy as np
import math
from print_settings import *
import print_settings
import console


class Path:
    count = 0
    def __init__(self, x=0, y=0, z=0, rot=None, tilt=None):
        self.path_number = Path.count
        Path.count += 1 
        kin_name, kinematics = print_settings.reload_print_setting()
        self.type = 'print'
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        if tilt is None:
            self.tilt = np.full_like(x, 0)
        else:
            self.tilt = np.array(tilt)
        if rot is None:
            self.rot = np.full_like(x, 0)
        else:
            self.rot = np.array(rot)
        kinematics.coords_arrange(self)
        self.set_print_settings()
        kinematics.e_calc(self)
        
    
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

class PathList:
    def __init__(self, paths):
        self.paths = paths
        self._extrusion_multiplier = None
        self._print_speed = None
        self._retraction = None
        self._z_hop = None
        self._before_gcode = None
        self._after_gcode = None
        if len(paths) != 0:
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

        # Extract first path and add to sorted list
        current_path = remaining_paths.pop(0)
        sorted_paths.append(current_path)

        while remaining_paths:
            nearest_index = None
            min_distance = float('inf')

            # Find the path with the closest starting point among unsorted paths
            for i, path in enumerate(remaining_paths):
                distance = np.linalg.norm(current_path.end_coord - path.start_coord)
                if distance < min_distance:
                    min_distance = distance
                    nearest_index = i

            # Retrieve the closest path and add it to the sorted list
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
    def move(arg, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        if isinstance(arg, Path):
            path = Transform.move_path(arg, x, y, z, roll, pitch, yaw)
            return path
        elif isinstance(arg, PathList):
            path_list = Transform.move_pathlist(arg, x, y, z, roll, pitch, yaw)
            return path_list
        
    @staticmethod
    def move_path(path,  x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        translation_vector = np.array([x, y, z])

        rotation_matrix = np.array([[np.cos(yaw) * np.cos(pitch),
                                    np.cos(yaw) * np.sin(pitch) * np.sin(roll) - np.sin(yaw) * np.cos(roll),
                                    np.cos(yaw) * np.sin(pitch) * np.cos(roll) + np.sin(yaw) * np.sin(roll)],
                                    [np.sin(yaw) * np.cos(pitch),
                                    np.sin(yaw) * np.sin(pitch) * np.sin(roll) + np.cos(yaw) * np.cos(roll),
                                    np.sin(yaw) * np.sin(pitch) * np.cos(roll) - np.cos(yaw) * np.sin(roll)],
                                    [-np.sin(pitch),
                                    np.cos(pitch) * np.sin(roll),
                                    np.cos(pitch) * np.cos(roll)]])

        path_coords = np.array(path.coords)

        translated_coords = path_coords + translation_vector

        transformed_coords = np.dot(rotation_matrix, np.transpose(translated_coords))

        x_coords = transformed_coords[0]
        y_coords = transformed_coords[1]
        z_coords = transformed_coords[2]

        moved_path = Path(x_coords, y_coords, z_coords)
        return moved_path
    @staticmethod
    def move_pathlist( pathlist, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        path_list_buffer = []
        for path in pathlist.paths:
            path = Transform.move_path(path,  x, y, z, roll, pitch, yaw)
            path_list_buffer.append(path)
        path_list_instance = PathList(path_list_buffer)
        path_list_buffer =[]
        return path_list_instance


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
                # closed curve
                p1 = polygon[(i-1)%(len(polygon)-1)]
                p2 = polygon[i%(len(polygon)-1)]
                p3 = polygon[(i+1)%(len(polygon)-1)]
            else:
                # open curve
                if i == 0:
                    # Processing of the starting point of an open curve
                    p1 = 2 * polygon[i] - polygon[i+1]
                    p2 = polygon[i]
                    p3 = polygon[i+1]
                elif i == len(polygon)-1:
                    # End of open curve
                    p1 = polygon[i-1]
                    p2 = polygon[i]
                    p3 = 2 * polygon[i] - polygon[i-1]
                else:
                    # Midpoint of open curve
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





