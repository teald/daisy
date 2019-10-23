'''
This file defines the basic Daisy object.

It should only contain the self-contained Daisy model, that ignores the other
Daisies in the world connected via other metrics.
'''
# Imports
import numpy as np
import constants as c
import pdb


# Class
class Daisy(object):
    '''
    This contains the Daisy class (edit this later!!!)
    '''

    def __init__(self, P, gamma, a_w, a_b, T):
        '''
        Initializes the Daisy class.

        Args:
            + P (float): the fertile area the daisies have to grow.
            + gamma (float): the death rate of the daisies in daisies/day.
            + a_w (float): area of P covered by white daisies.
            + a_b (float): area of P covered by black daisies
            + T (float): the surface temperature in Kelvin
        '''
        # Make all inputs other than self attributes
        self.P = P
        self.gamma = gamma
        self.a_w = a_w
        self.a_b = a_b
        self.T = T

        # Initialize the other parameters
        self.growthRate(T)
        self.emptySpace()
        self.albedo()


    def growthRate(self, T = None, test = False):
        '''
        Determines the growth rate (beta). If T != None (default), uses the
        given T. It will always return beta, but will only assign it as an
        attribute if test = False (default).

        Args:
            + T (float or None): If None (default), uses self.T. If a float,
                uses that value. Assumes the temperature is in Kelvin.
            + test (bool): If False (Default), will assign the calculated beta
                to self.beta. Otherwise, it will *only* return beta and not also
                assign it.

        Returns:
            + beta (float): The growth rate of the daisies.
        '''
        if T == None:
            beta = 1 - 3.265e-3 * (295.65 - self.T)**2.

        else:
            beta = 1 - 3.265e-3 * (295.65 - T)**2.

        if test: self.beta = beta
        return beta


    def emptySpace(self):
        '''
        Determines "x", the remaining area without daisies.
        '''
        self.x = self.P - self.a_w - self.a_b
        return self.x


    def albedo(self):
        '''
        Determines the albedo of this patch.
        '''
        self.A = self.x * c.surf_A + self.a_w * c.w_A + self.a_b * c.b_A
        return self.A


    def temperature(self):
        '''
        Determines the temperature and changes it given the current values.
        '''
        self.Teff = np.power(c.S * c.L * (1. - self.A) / c.sigma, 1/4)
        return self.Teff
