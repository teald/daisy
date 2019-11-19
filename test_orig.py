import pdb
from daisy import *
import matplotlib.pyplot as plt
import numpy as np

# Reproduce the plots from the OG daisyworld paper
a_types = np.array([0.1, 0.1])
A_types = np.array([c.A_w, c.A_b])
h = 0.1
dL = 0.01
Ls = np.arange(0.6, 1.6 + dL, dL)
N = len(Ls)
pops = np.zeros((N, len(a_types)))
Ts = np.zeros_like(Ls)

pops[0] = np.zeros_like(a_types) + 0.01

for i, L in enumerate(Ls[:-1]):
    # Initial guess is last step
    a_0 = np.where(pops[i] < 0.01, 0.01, pops[i])

    # Make new daisy object for this solution
    d_cur = Daisy(1, 0.3, a_0, A_types, L)

    # Solve
    d_cur.rk4Solve(100000, h)

    pops[i+1] = d_cur.a_vec[:-1]
    Ts[i+1] = d_cur.Teff
    print(f'L = {L:1.1f}', end=' || ')
    for i, p in enumerate(pops[i+1]):
        print(f'p_{i} = {p:1.2e}', end=' || ')
    print(f'total = {np.sum(pops[i+1,:]):1.2e}',end='\n')

fig, axes = plt.subplots(2,1)
ax = axes.flatten()[0]
ax.plot(Ls, pops[:,0]*100, 'b-', label='White daisy fraction')
ax.plot(Ls, pops[:,1]*100, 'k-', label='Black daisy fraction')
ax.set_ylabel('Daisy area (%)')
ax.set_ylim([0,100])
ax.legend(loc='best')

ax = axes.flatten()[1]
ax.set_ylabel('Temperature (deg. Celcius)')
ax.set_xlabel('Solar Luminosity Fraction')
ax.plot(Ls, Ts - 273.25, 'b-')
ax.set_ylim([-10., 70.])

fig.tight_layout()

plt.savefig('daisy_paper_d.png')

# Testing all parts of fig 1
## Part a
print("\n\nNeutral daisy run")
a_types = np.array([0.1])
A_types = np.array([0.5])
pops = np.zeros((N, len(a_types)))

Ts = np.zeros_like(Ls)

pops[0] = np.zeros_like(a_types) + 0.01

for i, L in enumerate(Ls[:-1]):
    # Initial guess is last step
    a_0 = np.where(pops[i] < 0.01, 0.01, pops[i])

    # Make new daisy object for this solution
    d_cur = Daisy(1, 0.3, a_0, A_types, L)

    # Solve
    d_cur.rk4Solve(100000, h)

    pops[i+1] = d_cur.a_vec[:-1]
    Ts[i+1] = d_cur.Teff
    print(f'L = {L:1.1f} || a_b = {pops[i+1,0]:1.2e}', end='\r')

print(end='\n')
print("Neutral daisy run completed")

fig, axes = plt.subplots(2,1)
ax = axes.flatten()[0]
ax.plot(Ls, pops[:,0]*100, 'b-', label='Neutral daisy fraction')
ax.set_ylabel('Daisy area (%)')
ax.set_ylim([0,100])
ax.legend(loc='best')

ax = axes.flatten()[1]
ax.set_ylabel('Temperature (deg. Celcius)')
ax.set_xlabel('Solar Luminosity Fraction')
ax.plot(Ls, Ts - 273.25, 'b-')
ax.set_ylim([-10., 70.])

fig.tight_layout()

plt.savefig('daisy_paper_a.png')

## Part b
print("\n\nBlack daisy run")
a_types = np.array([0.1])
A_types = np.array([0.25])
pops = np.zeros((N, len(a_types)))

Ts = np.zeros_like(Ls)

pops[0] = np.zeros_like(a_types) + 0.01

for i, L in enumerate(Ls[:-1]):
    # Initial guess is last step
    a_0 = np.where(pops[i] < 0.01, 0.01, pops[i])

    # Make new daisy object for this solution
    d_cur = Daisy(1, 0.3, a_0, A_types, L)

    # Solve
    d_cur.rk4Solve(100000, h)

    pops[i+1] = d_cur.a_vec[:-1]
    Ts[i+1] = d_cur.Teff
    print(f'L = {L:1.1f} || a_b = {pops[i+1,0]:1.2e}', end='\r')

print(end='\n')
print("Black daisy run finished")

fig, axes = plt.subplots(2,1)
ax = axes.flatten()[0]
ax.plot(Ls, pops[:,0]*100, 'k-', label='Black daisy fraction')
ax.set_ylabel('Daisy area (%)')
ax.set_ylim([0,100])
ax.legend(loc='best')

ax = axes.flatten()[1]
ax.set_ylabel('Temperature (deg. Celcius)')
ax.set_xlabel('Solar Luminosity Fraction')
ax.plot(Ls, Ts - 273.25, 'b-')
ax.set_ylim([-10., 70.])

fig.tight_layout()

plt.savefig('daisy_paper_b.png')

## Part c
print("\n\nWhite daisy run")
a_types = np.array([0.1])
A_types = np.array([0.75])
pops = np.zeros((N, len(a_types)))

Ts = np.zeros_like(Ls)

pops[0] = np.zeros_like(a_types) + 0.01

for i, L in enumerate(Ls[:-1]):
    # Initial guess is last step
    a_0 = np.where(pops[i] < 0.01, 0.01, pops[i])

    # Make new daisy object for this solution
    d_cur = Daisy(1, 0.3, a_0, A_types, L)

    # Solve
    d_cur.rk4Solve(100000, h)

    pops[i+1] = d_cur.a_vec[:-1]
    Ts[i+1] = d_cur.Teff
    print(f'L = {L:1.1f} || a_w = {pops[i+1,0]:1.2e}', end='\r')

print(end='\n')
print('White daisy run finished')

fig, axes = plt.subplots(2,1)
ax = axes.flatten()[0]
ax.plot(Ls, pops[:,0]*100, 'g-', label='White daisy fraction')
ax.set_ylabel('Daisy area (%)')
ax.set_ylim([0,100])
ax.legend(loc='best')

ax = axes.flatten()[1]
ax.set_ylabel('Temperature (deg. Celcius)')
ax.set_xlabel('Solar Luminosity Fraction')
ax.plot(Ls, Ts - 273.25, 'b-')
ax.set_ylim([-10., 70.])

fig.tight_layout()

plt.savefig('daisy_paper_c.png')

plt.show()

