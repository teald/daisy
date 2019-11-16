#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:43:15 2019

@author: ekhammer
"""

import numpy as np
from daisy import Daisy


class Parcel(Daisy):

    def _updatetemp(self, temp1, temp2, temp3, temp4, eff1, eff2, eff3, eff4):
        '''Updates parcel parameters in the correct order'''
        temps = np.array([temp1, temp2, temp3, temp4])
        effs = np.array([eff1, eff2, eff3, eff4])
        dT = (temps - self.Teff) / effs
        self.Teff = self.Teff - np.sum(dT)
        return self.Teff

    def Lfrac(self, theta, long):
        '''Calculates luminosity fraction based on theta'''
        self.theta = theta
        self.long = long
        return np.cos(90-self.theta)
