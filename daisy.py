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

    def __init__(self, P, gamma, a_vec, A_vec, L=1.0, T_vec=None,
                 verbose=False, A_g=0.5, S=c.S, q=c.q):
        '''
        Initializes the Daisy class. All parameters except gamma (a constant)
        are the initial conditions that will change as the daisies are
        integrated in time using Daisy().solve().

        Args:
            + P (float): the fertile area the daisies have to grow.
            + gamma (float): the death rate of the daisies in daisies/day.
            + a_vec (array): the numpy 1D array containing the fractional area
                covered by each desired species of daisy
            + A_vec (array): the numpy 1D array containing the albedos of each
                daisy species in a_vec
            + L (float): the fraction of solar flux incident on the surface
                (where S = 9.17e5 erg/cm^2/s is the solar flux at Earth's
                surface.
            + T_vec (array or None): the numpy 1D array of optimal temperatures
                for each daise species. If None (default) uses the default
                optimal daisy temperature from Watson & Lovelock 1983.
            + verbose (bool): if True, prints out A LOT. If False (default) it
                will not do that.
            + A_g (float): albedo of the ground for fraction of land not
                covered by daisies. Default 0.5
            + S (float): The solar surface flux in erg/cm^2/s (default c.S,
                from the constants file).
            + q (float or arr): The absorption efficiency of the daisies and
                ground (default c.q).
        '''
        # Make all inputs other than self attributes
        self.P = P
        self.gamma = gamma
        self.in_a_vec = a_vec  # The input vector, to be modified
        self.in_A_vec = A_vec  # The input vector, to be modified
        self.T_vec = T_vec     # The input vector, to be modified
        self.L = L
        self.verbose = verbose
        self.S = S
        self.q = q

        # Create the full arrays, including the ground and its albedo
        self.a_vec = np.array([ai for ai in (a_vec.tolist() +
                                             [P-np.sum(a_vec)])])
        self.A_vec = np.array([Ai for Ai in (A_vec.tolist() + [A_g])])

        # Initialize other vectors
        self.T = np.zeros_like(self.a_vec)

        # Check for input temperatures
        if T_vec is None:
            self.T_vec = 295.65
        else:
            # Adding in the ground
            self.T_vec = np.asarray(self.T_vec.tolist() + [295.65])

        # Initialize the other parameters
        self.update()

    def update(self, a_vec=None):
        '''Updates daisy parameters in the correct order'''
        self.daisy_check()
        self.emptySpace(a_vec)
        self.albedo(a_vec)
        self.temperature()
        self.growthRate()

    def daisy_check(self):
        '''
        Checks to make sure no daisy populations are negative, and that all
        daisy populations are less than 1.
        '''
        self.a_vec = np.where(self.a_vec < 1e-16, 1e-15, self.a_vec)
        #self.a_vec /= np.linalg.norm(self.a_vec)

    def growthRate(self):
        '''
        Determines the growth rate (beta). If T != None (default), uses the
        given T. It will always return beta, but will only assign it as an
        attribute if test = False (default).
        '''
        self.beta = 1 - 3.265e-3 * (self.T_vec - self.T)**2.
        return self.beta

    def emptySpace(self, a_vec=None):
        '''
        Determines "x", the remaining area without daisies.
        '''
        if a_vec is None:
            self.x = self.P - np.sum(self.a_vec[:-1])
            self.a_vec[-1] = self.x
        else:
            self.x = self.P - np.sum(a_vec[:-1])
            self.a_vec[-1] - self.x
        return self.x

    def albedo(self, a_vec=None):
        '''
        Determines the albedo of this patch.
        '''
        if a_vec is None:
            self.A = self.a_vec@self.A_vec
        else:
            self.A = a_vec@self.A_vec
        return self.A

    def T_i(self, A=None):
        '''
        Calculates individual daisy temperatures as a function of albedo.
        '''
        if A is None:
            return np.power(c.q * (self.A - self.A_vec) + self.Teff**4, 1/4)
        else:
            return np.power(c.q * (self.A - A) + self.Teff**4, 1/4)

    def temperature(self):
        '''
        Determines the temperature and changes it given the current values.
        '''
        self.Teff = np.power(self.S * self.L * (1. - self.A) / c.sigma, 1/4)

        # These comments right now are for testing
        #print('\n\n')
        #for key, item in self.__dict__.items():
        #    print(f'{key} = {item}')

        if np.isnan(self.A):
            print('\n\n')
            for key, item in self.__dict__.items():
                print(f'{key} = {item}')
            pdb.set_trace()

        # Temperature array with Teff standing in for the ground question
        self.T[:-1] = self.T_i(self.A_vec[:-1])
        self.T[-1] = self.Teff
        return self.T

    def dDaisies(self, r, t, x, beta, gamma):
        '''
        Differential equations to be solved for the daisy object.
        '''
        da = r * (beta * x - gamma)
        # Handle ground
        da[-1] = 0.
        return da

    def rk4Solve(self, maxsteps, h, autostop=True, onestep=False):
        '''
        Implements the 4th-order Runga-Kutta method for solving differential
        equations.

        Args:
            + maxsteps (float): maximum number of steps to take
            + h (float): the step size (is this what it's formally called?)
            + func (function): The function that defines the differential
                system.
            + args (iterable): Arguments as an iterable to be passed to func
                after r0 and t. Default [], which implies no additional
                arguments.
            + autostop (bool, default True): if True, will stop when the change
                each iteration is less than 1e-6.
            + onestep (bool, default False): if True, will only step forward
                once in the rk4 solver instead of waiting for time convergence.
                This *overrides autostop*.

        Returns:
            + ts (array): the array of times integrated over
            + rs (array): array containing the integration itself over time.
        '''
        args = [self.x, self.beta, self.gamma]
        # Only perform one step if onestep
        if onestep:
            t = 0
            r = self.a_vec
            k1 = h * self.dDaisies(r, t, *args)
            self.update(r + 0.5 * k1)
            k2 = h * self.dDaisies(r + 0.5 * k1, t + 0.5*h, *args)
            self.update(r + 0.5 * k2)
            k3 = h * self.dDaisies(r + 0.5 * k2, t + 0.5*h, *args)
            self.update(r + k3)
            k4 = h * self.dDaisies(r + k3, t + h, *args)
            r = r + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
            self.a_vec = r
            self.update()
            return r

        # Create the ts and rs
        ts = np.linspace(0, 1000., maxsteps)
        r0 = self.a_vec
        rs = np.zeros((len(ts), len(r0)))
        rs[0, :] = r0

        # Useful output
        areas = self.a_vec * self.P
        if self.verbose:
            print(f'Beginning daisy integration...')
            for i, area in enumerate(areas):
                print(f'area {i}: {area:1.3e}', end=' || ')
            print(f'Tsurf = {self.Teff:.3f}', end='\n')

        # use cur_r if autostop is enabled
        if autostop:
            cur_r = r0
            prev_Teff = -100000

        # 4th-order Runga Kutta integration
        dr = 1e6
        for i, t in enumerate(ts[:-1]):
            # 4th order Runga-Kutta integration step
            k1 = h * self.dDaisies(rs[i], t, *args)
            self.update(rs[i] + 0.5 * k1)
            k2 = h * self.dDaisies(rs[i] + 0.5 * k1, t + 0.5*h, *args)
            self.update(rs[i] + 0.5 * k2)
            k3 = h * self.dDaisies(rs[i] + 0.5 * k2, t + 0.5*h, *args)
            self.update(rs[i] + k3)
            k4 = h * self.dDaisies(rs[i] + k3, t + h, *args)
            rs[i+1] = rs[i] + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Update the daisy pop attributes
            self.a_vec = rs[i+1]

            # Recalculate the new physical parameters for the daisies.
            self.update()

            # Print out the current step
            areas = self.a_vec * self.P
            if self.verbose:
                for i, area in enumerate(areas):
                    print(f'area {i}: {area:1.3e}', end=' || ')
                print(f'Tsurf = {self.Teff:.3f}', end='\n')

            if autostop:
                # Check for convergence
                dr = np.absolute(np.linalg.norm(rs[i+1]-cur_r))
                dr = np.amax(np.absolute(rs[i+1] - cur_r))
                dT = np.absolute(self.Teff - prev_Teff)
                if np.amax([dr, dT]) < 1e-4:
                    if self.verbose:
                        print("Converged!")

                    break

                # Update cur_r for next dr comparison
                cur_r = rs[i+1]
                dT = np.absolute(self.Teff - prev_Teff)
                prev_Teff = self.Teff

            args = [self.x, self.beta, self.gamma]

        return ts, rs
