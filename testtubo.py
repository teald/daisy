# Imports
from tube import Tube
import numpy as np
import constants as c
import matplotlib.pyplot as plt

# Initialize a tube
tube = Tube(1, 0.3, np.array([0.1, 0.1]), np.array([c.A_w, c.A_b]))
tube.setupGrid(10, 10, 70)
tube._updategrid()
plt.figure()
tube.plot()
tube._updategrid()
tube._updategrid()
tube._updategrid()
plt.figure()
tube.plot()
tube._updategrid()
tube._updategrid()
tube._updategrid()
plt.figure()
tube.plot()
plt.show()
