# imports
import matplotlib.pyplot as plt
import numpy as np

from tube import Tube

# Make the file on the fly
m = 40
n = 30
water = 5

grid = []
for r in range(n):
    row = []
    for c in range(m):
        if water > c  or c >= m - water:
            row.append('o')
        else:
            row.append('x')
    grid.append(row)

with open('test.world', 'w+') as outfile:
    for row in grid:
        outstr = ''
        for c in row:
            outstr += f'{c} '
        outstr += '\n'
        outfile.write(outstr)

# Test different daisy numbers
def test_ndaisies(n_daisies):
    P = 1
    gamma = 0.3
    a_vec = np.array([1/(n_daisies + 1) for i in range(n_daisies)])
    #A_vec = np.random.uniform(0, 0.5, size=n_daisies)
    A_vec = np.linspace(0.05, 0.75, n_daisies)
    T_vec = np.random.normal(295., 10., size=n_daisies)
    #T_vec = 295 * np.ones(n_daisies)
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
        tube.setupGrid(0, 0, 80, oceans=True, inputfile='test.world')

        #tube.plot(r'Daisyworld init', ptype='albedo')

        for i in range(100):
            print(f"{i}")
            tube._updategrid()

    tube.plot(f"Daisyworld w/ {n_daisies} daisies")
    tube.plot(f"Daisyworld w/ {n_daisies} daisies", ptype='albedo')


for n in [2, 5, 25, 50]:
    test_ndaisies(n)
plt.show()
