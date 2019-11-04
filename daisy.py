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

    def __init__(self, P, gamma, a_w, a_b):
        '''
        Initializes the Daisy class. All parameters except gamma (a constant)
        are the initial conditions that will change as the daisies are
        integrated in time using Daisy().solve().

        Args:
            + P (float): the fertile area the daisies have to grow.
            + gamma (float): the death rate of the daisies in daisies/day.
            + a_w (float): area of P covered by white daisies.
            + a_b (float): area of P covered by black daisies
        '''
        # Make all inputs other than self attributes
        self.P = P
        self.gamma = gamma
        self.a_w = a_w
        self.a_b = a_b

        # Initialize the other parameters
        self.update()

    def update(self):
        '''Updates daisy parameters in the correct order'''
        self.emptySpace()
        self.albedo()
        self.temperature()
        self.growthRate()

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

        if not test: self.beta = beta
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
        self.Teff = np.power(c.q * 1. - self.A, 1/4)
        # Calculate the individual daisy temperatures as a function of albedo
        T_i = lambda A: np.power(q * (self.A - A) + self.Teff**4, 1/4)

        self.T= np.array([T_i(c.w_A), T_i(c.b_A)])
        return self.T


    def dDaisies(self, r, t, x, beta, gamma):
        '''
        Differential equations to be solved for the daisy object.
        '''
        da = r * (beta * x - gamma)
        return da


    def rk4Solve(self, t0, tf, h, autostop=True):
        '''
        Implements the 4th-order Runga-Kutta method for solving differential
        equations.

        Args:
            + t0 (float): start time for the integration
            + tf (float): end time for the integration
            + h (float): the step size (is this what it's formally called?)
            + func (function): The function that defines the differential
                system.
            + args (iterable): Arguments as an iterable to be passed to func
                after r0 and t. Default [], which implies no additional
                arguments.
            + autostop (bool, default True): if True, will stop when the change
                each iteration is less than 1e-14.

        Returns:
            + ts (array): the array of times integrated over
            + rs (array): array containing the integration itself over time.
        '''
        # Create the ts and rs
        ts = np.arange(t0, tf + h, h)
        r0 = np.array([self.a_w, self.a_b], dtype=float)
        rs = np.zeros((len(ts), len(r0)))
        rs[0] = r0

        # Set up the function to use
        func = lambda r, t: self.dDaisies(r, t, self.x, self.beta, self.gamma)

        # Useful output
        print(f'Beginning daisy integration...')
        print(f'a_w = {self.a_w:1.3e} || a_b = {self.a_b:1.3e} || '
              f'Tsurf = {self.T}')

        # 4th-order Runga Kutta integration
        dr = 1e6
        cur_r = r0
        for i, t in enumerate(ts[:-1]):
            k1 = h * func(rs[i], t)
            k2 = h * func(rs[i] + 0.5 * k1, t + 0.5*h)
            k3 = h * func(rs[i] + 0.5 * k2, t + 0.5*h)
            k4 = h * func(rs[i] + k3, t + h)
            rs[i+1] = rs[i] + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Update the attributes
            self.a_w, self.a_b = rs[i+1]

            # Recalculate the new physical parameters for the daisies.
            self.update()

            # Print out the current step
            print(f'a_w = {self.a_w:1.3e} || a_b = {self.a_b:1.3e} || '
                  f'Tsurf = {self.T}')

            if autostop:
                # Check for convergence
                dr = np.absolute(np.linalg.norm(rs[i+1]-cur_r))
                if dr < 1e-14:
                    print("Converged!")
                    break
                cur_r = rs[i+1]

        return ts, rs
