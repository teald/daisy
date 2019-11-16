#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:43:15 2019

@author: ekhammer
"""

import numpy as np
import constants as c
import pdb
from daisy import Daisy


class Parcel(Daisy):

    def _updatetemp(self, temp1, temp2, temp3, temp4):
        '''Updates parcel parameters in the correct order'''
        # some equation????
        pass

    def Lfrac(self, theta, long):
        '''Calculates luminosity fraction based on theta'''
        self.theta = theta
        self.long = long
        return np.cos(90-self.theta)
    
        
        
    
        