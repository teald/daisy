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
        gridpos = np.empty([m,n])

        thetas =  #array like gridpos
##self.gridpos = np.
        #self.npix = hp.nside2npix(self.n)
        #self.grid = np.arange(npix)

    def __update(self, ):
        '''
        Update Parcel parameters for grid.
        '''
        for i in self.grid:
            continue
        # Do Parcel stuff
        pass


# If parcel is on top or bottom then just pass temp from edge as temp in parcel

    def plot(self):
        #plot the grid
        hp.cartview(self.grid)
        pass
