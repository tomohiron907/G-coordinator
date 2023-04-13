import numpy as np
import math
import matplotlib.pyplot as plt


class Path:
    def __init__(self, x=0, y=0, z=0):
        self.type = 'print'
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self.coords_arrange()
        self.set_print_settings()
        
    def coords_arrange(self):
        self.coords = np.column_stack([self.x, self.y, self.z])
        return self.coords
    
    def set_print_settings(self):
        self.E_multiplier = 1
        self.E_multiplier_array = np.full_like(self.x, 1)
        self.feed = 1000
        self.feed_array = np.full_like(self.x, 1000)
        self.retract = False
        self.before_gcode = ''
        self.after_gcode = ''


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




def plot_path(path):
    plt.plot(path.coords[:,0], path.coords[:,1])
    
    
    
    
def object_modeling():
    arg = np.linspace(0, 2*np.pi, 100)
    r = 2
    x = r * np.cos(arg)
    y = r * np.sin(arg)
    z = np.full_like(x, 0)
    path = Path(x, y, z)
    plot_path(path)
    offset_path = Transform.offset(path, 0.1)
    bottom = Transform.fill(path, infill_distance = 0.1, offset = 0.2)
    bottom_rotate = Transform.rotate(bottom, np.pi/2)
    plot_path(offset_path)
    plot_path(bottom)
    plot_path(bottom_rotate)
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    object_modeling()
