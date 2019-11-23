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
        self.n = n #width
        self.m = m #height
        self.maxtheta = maxtheta #max latitude to use
        self.deltheta = self.maxtheta / (0.5 * m) #theta resolution
        self.npix = n * m
        self.gridpos = np.empty([m,n]) #starting temperatures (to be fixed)
        self.thetas = np.ones([m,n]) * np.linspace(maxtheta, -maxtheta, m) #array like gridpos (to be fixed)
##self.gridpos = np.
        #self.npix = hp.nside2npix(self.n)
        #self.grid = np.arange(npix)

    def __update(self, grid):
        '''
        Update Parcel parameters for grid.
        '''
        for m,n in self.grid: #go left to right (West to East)
            #change to for loop with arrays
            if m = 0:
                T_t = grid[m,n]
            else:
                T_t = grid[m-1,n]
            if m = len(grid[:,n]) - 1:
                T_b = grid[m,n]
            else:
                T_b = grid[m+1,n]
            if n = 0:
                T_l = grid[m,-1:]
            else:
                T_l = grid[m,n-1]
            if n = len(grid[m,:]) - 1:
                T_r = grid[m,0]
            else:
                T_r = grid[m,n+1]

            grid[i,j] = Parcel(args)
        # Do Parcel stuff
        


# If parcel is on top or bottom then just pass temp from edge as temp in parcel

    def plot(self):
        #plot the grid
        #hp.cartview(self.grid)
        plt.imshow(self.grid)
        plt.grid()
