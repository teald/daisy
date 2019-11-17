'''
This file defines the TUBE.

Bow down to the TUBE and it may show mercy upon your soul.
'''

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

import constants as c
from daisy import Daisy
from parcel import Parcel

class Tube(Daisy, Parcel):
    '''
    This contains the Tube class.
    '''

    def setupGrid(self, n):
        self.n = n
        self.npix = hp.nside2npix(self.n)

    def __update(self, ):
        '''
        Update Parcel parameters for grid.
        '''
        #do Parcel stuff
        pass


#if parcel is on top or bottom then just pass temp from edge as temp in parcel
