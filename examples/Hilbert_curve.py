import numpy as np
import gcoordinator as gc

def hilbert_curve(x, y, xi, xj, yi, yj, depth):
    if depth <= 0:
        return [x + (xi + yi) / 2], [y + (xj + yj) / 2]
    
    xn = x + (xi + yi) / 2
    yn = y + (xj + yj) / 2
    
    x1, y1 = hilbert_curve(x, y, yi / 2, yj / 2, xi / 2, xj / 2, depth - 1)
    x2, y2 = hilbert_curve(x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, depth - 1)
    x3, y3 = hilbert_curve(x + xi / 2 + yi / 2, y + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, depth - 1)
    x4, y4 = hilbert_curve(x + xi / 2 + yi, y + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, depth - 1)
    
    return x1 + x2 + x3 + x4, y1 + y2 + y3 + y4

def draw_hilbert_curve(length, depth, height):
    x = 0
    y = 0
    xi = length
    xj = 0
    yi = 0
    yj = length
    
    x, y = hilbert_curve(x, y, xi, xj, yi, yj, depth)
    z = np.full_like(x, 0.2*height + 0.2)
    hilbert = gc.Path(x, y, z)
    return hilbert

full_object=[]
for height in range(10):
    hilbert = draw_hilbert_curve(200, 6, height * 0.2)
    hilbert = gc.Transform.move(hilbert, -100, -100)
    full_object.append(hilbert)

gc.gui_export(full_object)
