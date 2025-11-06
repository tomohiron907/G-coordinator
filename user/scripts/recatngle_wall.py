import gcoordinator as gc
full_object = []

for height in range(100):
    x = [0, 10.0, 10.0, 0, 0]
    y = [0, 0, 10.0, 10.0, 0]
    z = [(height+1)*0.2] * 5
    path = gc.Path(x, y, z)
    full_object.append(path)
gc.gui_export(full_object)  # for G-coordinator (GUI app)