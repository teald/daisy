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
A_vec = np.random.uniform(0.05, 0.85, size=n_daisies)
A_vec = np.linspace(0.25, 0.75, n_daisies)
T_vec = np.random.normal(295., 10., size=n_daisies).sort()
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

    tube.plot(r'Daisyworld init', savefig="temps_init.png")
    tube.plot(r'Daisyworld init albedos', ptype='albedo', savefig='albedos_init.png')
    #tube.plot(r'Daisyworld init', ptype='albedo')

    for i in range(100):
        print(f"{i}", end="\r")
        tube._updategrid()
        tube.plot(f'Daisyworld at {i} iterations',
                savefig=f'figures/frame_{i:03d}.png',
                ptype='temperature')
        tube.plot(f'Daisyworld at {i} iterations',
                savefig=f'figures/pop_frame_{i:03d}.png',
                ptype='pops')
        tube.plot(f'Daisyworld at {i} iterations',
                savefig=f'figures/pop_frame_{i:03d}.png',
                ptype='albedo')
        for ndaisy in range(n_daisies):
            tube.plot(f'Daisyworld at {i} iterations',
                    savefig=f'figures/pop_frame_{ndaisy}_{i:03d}.png',
                    ptype=f'{ndaisy}')


        #if i % 10 == 0 and i > 1:
        #    tube.plot(r'Daisyworld at {i} iterations')

tube.plot(r"Daisyworld Temperatures", savefig="temps_final.png")
tube.plot(f"Daisyworld Albedos",
          ptype='albedo', savefig="albedos_final.png")
tube.plot(r"Final daisy population fraction per parcel area", ptype="pops",
          savefig="pops_final.png")
#tube.plot(r"Daisyworld Temps with a %.2f $\pi$ Seasonal Phase" % (phi/np.pi),
#          ptype='albedo')

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
