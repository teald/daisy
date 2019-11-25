'''
This file defines the TUBE.

Bow down to the TUBE and it may show mercy upon your soul.
'''
# Imports
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

import constants as c
from daisy import Daisy
from parcel import Parcel


# Tube definition
class Tube(object):
    '''
    This contains the Tube class.
    '''

    def __init__(self, P, gamma, a_vec, A_vec):
        self.P = P
        self.gamma = gamma
        self.a_vec = a_vec
        self.A_vec = A_vec

    def setupGrid(self, n, m, maxtheta):
        self.n = n  # width
        self.m = m  # height
        self.maxtheta = maxtheta  # max latitude to use
        self.deltheta = self.maxtheta / (0.5 * m)  # theta resolution
        self.npix = n * m
        self.thetas = (np.ones([m, n]) * np.linspace(maxtheta, -maxtheta, m)
                       [:, np.newaxis])
        self.Ls = np.cos(90 - self.thetas.reshape(self.npix))

        grid = []
        for i in range(m * n):
            grid.append(Parcel(self.P, self.gamma, self.a_vec, self.A_vec, 
                               self.Ls[i]))
        self.grid = np.reshape(grid, (m, n))

    def _updategrid(self):
        '''
        Update Parcel parameters for grid.
        '''
        Temps = np.empty([self.m, self.n])

        for m in range(len(self.grid[:,0])):
            for n in range(len(self.grid[0,:])):# go left to right (West to East)
            # change to for loop with arrays
                if m == 0:
                    T_t = self.grid[m, n].Teff
                else:
                    T_t = self.grid[m-1, n].Teff
                if m == len(self.grid[:, n]) - 1:
                    T_b = self.grid[m, n].Teff
                else:
                    T_b = self.grid[m+1, n].Teff
                if n == 0:
                    T_l = self.grid[m, -1:].Teff
                else:
                    T_l = self.grid[m, n-1].Teff
                if n == len(self.grid[m, :]) - 1:
                    T_r = self.grid[m, 0].Teff
                else:
                    T_r = self.grid[m, n+1].Teff

                self.grid[m, n].update(T_t, T_b, T_l, T_r)

                Temps[m, n] = self.grid[m,n].Teff
        
        f = open("output.txt", "a")
        np.savetxt(f, Temps)
        f.write('\n'))
        f.write('DAISIES \n')
        f.close()

    def plot(self):
        #plot the grid
        temps = np.loadtxt("outputs.txt")
        plt.imshow(temps[0])
        plt.grid()
