import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =2

th = math.pi * 60 / 180  

R = 40
th = math.pi * 60 / 180
a = (0.0, 0.0) 
b = (R, 100.0 * math.sin(th) * R / 50) 
c = (2 * R, 0.0)

n = 7
points = [a] 


def koch(a, b, n):
    global points
    if n == 0:
        return
    s = (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3)
    t = (a[0] + (b[0] - a[0]) * 2 / 3, a[1] + (b[1] - a[1]) * 2 / 3)
    u = (s[0] + (t[0] - s[0]) * math.cos(th) - (t[1] - s[1]) * math.sin(th),s[1] + (t[0] - s[0]) * math.sin(th) + (t[1] - s[1]) * math.cos(th))
    koch(a, s, n - 1)
    points.append(s)
    koch(s, u, n - 1)
    points.append(u)
    koch(u, t, n - 1)
    points.append(t)
    koch(t, b, n - 1)

def object_modeling():
    global points
    full_object=[]
    for height in range(LAYER):
        points = [a]
        koch(a, b, n)
        points.append(b)
        koch(b, c, n)
        points.append(c)
        koch(c, a, n)
        points.append(a)
        x = [points[i][0] - R for i in range(len(points) - 1)]
        y = [points[i][1] - (R * math.sin(th / 2)) for i in range(len(points) - 1)] 
        z = np.full_like(x, height*0.2)
        wall = Path(x, y, z)
        #wall = Transform.rotate(wall, height)
        full_object.append(wall)
        


    return full_object
    

