# Imports
from tube import Tube
import numpy as np
import constants as c
import matplotlib.pyplot as plt

# Initialize a tube
n_daisies = 10
P = 1
gamma = 0.3
a_vec = np.array([1/(n_daisies + 1) for i in range(n_daisies)])
A_vec = np.random.uniform(0, 0.5, size=n_daisies)
T_vec = np.random.normal(295., 10., size=n_daisies)
#tube = Tube(P=1, gamma=0.3, 
            #a_vec=np.array([1/(n_daisies + 1) for i in range(n_daisies)]), 
            #A_vec=np.random.uniform(size=n_daisies), 
            #T_vec=np.random.normal(295., 10., size=n_daisies))
#tube.setupGrid(40, 40, 80)
#tube._updategrid()

#phis = [0, 1.57, 3.14, 4.71]
phis = np.linspace(-0.39, 0.39, 9)
phis = [0.]

for phi in phis:
    tube = Tube(P=P, gamma=gamma, a_vec=a_vec, A_vec=A_vec, phi=phi, T_vec=T_vec)
    tube.setupGrid(0, 0, 80, oceans=True, inputfile='harrison.world')

    tube.plot(r'Daisyworld init')
    #tube.plot(r'Daisyworld init', ptype='albedo')

    for i in range(10):
        print(f"{i}", end="\r")
        tube._updategrid()

        if i % 10 == 0 and i > 1:
            tube.plot(r'Daisyworld at {i} iterations')

tube.plot(r"Daisyworld Temps with a %.2f $\pi$ Seasonal Phase" % (phi/np.pi))
#tube.plot(r"Daisyworld Temps with a %.2f $\pi$ Seasonal Phase" % (phi/np.pi),
#          ptype='albedo')

plt.show()
'''
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
tube._updategrid()
tube._updategrid()
tube._updategrid()
tube._updategrid()
tube._updategrid()
plt.figure()
tube.plot()

for i in range(11):
    tube._updategrid()
    if i % 1 == 0:
        print(f"{i}", end='\r')
        plt.figure()
        tube.plot(title=(f"Daisyworld After {i} Iterations"))

plt.show()
'''
