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

    def __init__(self, P, gamma, a_w, a_b, L, verbose=False):
        '''
        Initializes the Daisy class. All parameters except gamma (a constant)
        are the initial conditions that will change as the daisies are
        integrated in time using Daisy().solve().

        Args:
            + P (float): the fertile area the daisies have to grow.
            + gamma (float): the death rate of the daisies in daisies/day.
            + a_w (float): area of P covered by white daisies.
            + a_b (float): area of P covered by black daisies
            + L (float): the fraction of solar flux incident on the surface
                (where S = 9.17e5 erg/cm^2/s is the solar flux at Earth's
                surface.
            + verbose (bool): if True, prints out A LOT. If False (default) it
                will not do that.
        '''
        # Make all inputs other than self attributes
        self.P = P
        self.gamma = gamma
        self.a_w = a_w
        self.a_b = a_b
        self.L = L
        self.verbose = verbose

        # Initialize the other parameters
        self.update()

    def update(self):
        '''Updates daisy parameters in the correct order'''
        self.emptySpace()
        self.albedo()
        self.temperature()
        self.growthRate()

    def growthRate(self):
        '''
        Determines the growth rate (beta). If T != None (default), uses the
        given T. It will always return beta, but will only assign it as an
        attribute if test = False (default).
        '''
        self.beta = 1 - 3.265e-3 * (295.65 - self.T)**2.
        return self.beta


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
        self.Teff = np.power(c.S * self.L * (1. - self.A) / c.sigma, 1/4)
        # Calculate the individual daisy temperatures as a function of albedo
        T_i = lambda A: np.power(c.q * (self.A - A) + self.Teff**4, 1/4)

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
        if self.verbose:
            print(f'Beginning daisy integration...')
            print(f'a_w = {self.a_w:1.3e} || a_b = {self.a_b:1.3e} || '
                  f'Tsurf = {self.Teff}')

        # use cur_r if autostop is enabled
        if autostop: cur_r = r0

        # 4th-order Runga Kutta integration
        dr = 1e6
        for i, t in enumerate(ts[:-1]):
            k1 = h * func(rs[i], t)
            k2 = h * func(rs[i] + 0.5 * k1, t + 0.5*h)
            k3 = h * func(rs[i] + 0.5 * k2, t + 0.5*h)
            k4 = h * func(rs[i] + k3, t + h)
            rs[i+1] = rs[i] + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Update the daisy pop attributes
            self.a_w, self.a_b = rs[i+1]

            # Recalculate the new physical parameters for the daisies.
            self.update()

            # Print out the current step
            area_w = self.a_w * self.P
            area_b = self.a_b * self.P
            #print(f'a_w = {self.a_w:1.3e} || a_b = {self.a_b:1.3e} || '
            #        f'Tsurf = {self.Teff:1.3e} || i = {i}')
            if self.verbose:
                print(f'area white: {area_w:.1e} || area black: {area_b:.1e} '
                      f'|| Tsurf = {self.Teff}')

            if autostop:
                # Check for convergence
                dr = np.absolute(np.linalg.norm(rs[i+1]-cur_r))
                if dr < 1e-14:
                    if self.verbose: print("Converged!")
                    break
                cur_r = rs[i+1]

        return ts, rs
