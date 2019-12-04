# Imports
import numpy as np


# Class definition
class Ocean(object):
    '''
    The Ocean object is like a daisy, but only returns static
    values of temperatures and other values. The ocean is constant, the ocean
    is pure.
    '''

    def __init__(self, temp):
        ''' Initalizes the Ocean class to some constant temperatures.'''
        self.temp = temp
        self.Teff = temp
        self.A = 0.1

    def update(*args):
        pass
