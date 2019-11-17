#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:43:15 2019

@author: ekhammer
"""

import numpy as np
from daisy import Daisy
import matplotlib.pyplot as plt


# Parcel definition
class Parcel(Daisy):

    def _updatetemp(self, temp1, temp2, temp3, temp4):
        '''Updates parcel parameters in the correct order.'''
        temps = np.array([temp1, temp2, temp3, temp4])
        dT = (temps - self.Teff)

        def gaussian(x):
            '''Temperature efficiency relation.'''
            return np.exp(-np.power(x, 2.) / (2 * np.power(25, 2.)))

        effs = 1 - gaussian(dT)

        self.Teff = self.Teff - np.sum(dT*effs)
        return self.Teff

    def Lfrac(self, theta, long):
        '''Calculates luminosity fraction based on theta.'''
        self.theta = theta
        self.long = long
        return np.cos(90-self.theta)


Teff = 300
temps = np.array([257, 0.0, 328, 291])
dT = (temps - Teff)


def gaussian(x):
    return np.exp(-np.power(x, 2.) / (2 * np.power(25, 2.)))


testDt = np.arange(-100, 100, 1)

plt.plot(testDt, 1-gaussian(testDt))
plt.show()


effs = 1 - gaussian(dT)

Teff = Teff + np.sum(dT*effs)
