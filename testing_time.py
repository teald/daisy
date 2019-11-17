import pdb
from daisy import *
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)

# Testing the Daisy object
Nds = 20
a_types = np.array([0.1 for i in range(Nds)])
A_types = np.array([(i+1)/Nds for i in range(Nds)])
T_types = np.random.normal(295., 10., size=a_types.shape)
T_types = None

# Step forward in time and plot that toward convergence
h = 0.1
dL = 0.01
ts = np.arange(0., 10000.+h, h)
Ls = .6 + np.power(np.sin(ts/(ts[-1] / 4)), 2)

pops = np.zeros((len(ts), len(a_types)))

pops[0] = np.zeros_like(a_types) + 0.01

# daisy object initialization
daisy = Daisy(1, 0.3, a_types, A_types, Ls[0], T_types)

for i, t in enumerate(ts[:-1]):
    # go one step forward
    daisy.L = np.copy(Ls[i])
    pops[i+1] = daisy.rk4Solve(0, h, onestep=True)[:-1]
    print(f'Iteration {i} of {len(ts)} done. {daisy.L}.')

# Plot the values as a function of time
figure, ax = plt.subplots()
cmap = plt.get_cmap('rainbow')
colors = [cmap(i/pops.shape[1]) for i in range(pops.shape[1])]
for c, d in zip(colors, range(pops.shape[1])):
    ax.plot(ts, pops[:,d], c=c, label=f'Daisy {d}')

ax.set_title(f'Daisyworld with L = {1}, Daisy number = {Nds}')
ax.set_xlabel('Time (meaningless)')
ax.set_ylabel('Daisy population (fraction)')
ax.set_title(f'Total area covered by daisies: {np.sum(pops[-1,:-1])}')
plt.show()
