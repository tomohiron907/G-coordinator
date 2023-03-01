import numpy as np
import math
#from shapely.geometry.polygon import LinearRing,LineString
import sys

def print_layer(x, y, z, Feed = None, E_multiplier = None):
    coordinates = np.column_stack([x,y,z]).tolist()
    
    if Feed is None:
        nans = np.zeros(len(coordinates))
        nans[:] = np.nan
        Feed_list = nans
    elif type(Feed) is np.ndarray:
        Feed_list = Feed
    else:
        Feed_list = np.full(len(coordinates),Feed)


    if E_multiplier is None:
        nans = np.zeros(len(coordinates))
        nans[:] = np.nan
        E_multiplier_list = nans
    elif type(E_multiplier) is np.ndarray:
        E_multiplier_list = E_multiplier
    else:
        E_multiplier_list = np.full(len(coordinates),E_multiplier)
    
    layer_list = np.column_stack([x,y,z,Feed_list,E_multiplier_list]).tolist()

    return layer_list

def travel_to(x, y, z, Feed = None, E_multiplier = None):
    coordinates = np.column_stack([x,y,z]).tolist()
    
    if Feed is None:
        nans = np.zeros(len(coordinates))
        nans[:] = np.nan
        Feed_list = nans
    elif type(Feed) is np.ndarray:
        Feed_list = Feed
    else:
        Feed_list = np.full(len(coordinates),Feed)


    if E_multiplier is None:
        nans = np.zeros(len(coordinates))
        nans[:] = np.nan
        E_multiplier_list = nans
    elif type(E_multiplier) is np.ndarray:
        E_multiplier_list = E_multiplier
    else:
        E_multiplier_list = np.full(len(coordinates),E_multiplier)
    
    layer_list = np.column_stack([x,y,z,Feed_list,E_multiplier_list]).tolist()

    return layer_list



def line_fill(a,distance,angle):
    x=[]
    y = []

    for i in range(len(a)):
        x.append(a[i][0])
        y.append(a[i][1])


    x=np.array(x)
    y= np.array(y)
    if angle == np.pi/2 or angle == -np.pi/2:
        angle -=0.001
    y_intersept = distance / math.cos(angle)
    K = np.arange(-200/math.cos(angle),200/math.cos(angle),y_intersept)
    Xlist=[]
    Ylist=[]
    
    
    slope = math.tan(angle)
    for k in K:
        for n in range(len(a)-1):
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
    Zlist = [a[0][2] for i in range(len(Xlist))]
    return Xlist,Ylist,Zlist


'''def contour_offset(layer,distance):
    x=[]
    y = []
    z = []
    for i in range(len(layer)):
        x.append(layer[i][0])
        y.append(layer[i][1])
        z.append(layer[i][2])
    x=np.array(x)
    y= np.array(y)
    z = np.array(z)
    pos_array = np.column_stack([x, y, z])
    poly_line = LineString(pos_array)
    poly_line_offset = poly_line.parallel_offset(distance, side='left', resolution=6, join_style=2, mitre_limit=1)
    Xlist = poly_line_offset.xy[0]
    Ylist = poly_line_offset.xy[1]
    Zlist = [pos_array[0][2] for i in range(len(Xlist))]
    offset_list = np.column_stack([Xlist,Ylist,Zlist])
    return Xlist,Ylist,Zlist'''


