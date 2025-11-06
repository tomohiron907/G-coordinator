import numpy as np
import gcoordinator as gc

x = np.array([0.0, 10.0, 10.0, 0.0, 0.0], dtype=float)
y = np.array([0.0, 0.0, 10.0, 10.0, 0.0], dtype=float)
z = np.zeros_like(x)

rectangle = gc.Path(x, y, z)
full_object = [rectangle]

gc.gui_export(full_object)  # for G-coordinator (GUI app)
