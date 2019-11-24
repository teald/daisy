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
class Tube(Parcel):
    '''
    This contains the Tube class.
    '''

    def setupGrid(self, n, m, maxtheta):
        self.n = n  # width
        self.m = m  # height
        self.maxtheta = maxtheta  # max latitude to use
        self.deltheta = self.maxtheta / (0.5 * m)  # theta resolution
        self.npix = n * m
        self.thetas = (np.ones([m, n]) * np.linspace(maxtheta, -maxtheta, m)
                       [:, np.newaxis])
        self.temps = (abs(self.thetas) / maxtheta) * 275 #to be fixed

        grid = []
        for i in range(m * n):
            grid.append(Parcel())
        self.grid = np.reshape(grid, (m, n))

    def _updategrid(self):
        '''
        Update Parcel parameters for grid.
        '''
        for m, n in self.grid:  # go left to right (West to East)
            # change to for loop with arrays
            if m == 0:
                T_t = self.grid[m, n]
            else:
                T_t = self.grid[m-1, n]
            if m == len(self.grid[:, n]) - 1:
                T_b = self.grid[m, n]
            else:
                T_b = self.grid[m+1, n]
            if n == 0:
                T_l = self.grid[m, -1:]
            else:
                T_l = self.grid[m, n-1]
            if n == len(self.grid[m, :]) - 1:
                T_r = self.grid[m, 0]
            else:
                T_r = self.grid[m, n+1]

            self.grid[i, j]._updatetemp(T_t, T_b, T_l, T_r)

    def plot(self):
        #plot the grid
        plt.imshow(self.grid)
        plt.grid()
