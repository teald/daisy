'''
This file defines the Parcel object.

It takes information from the Tube object (theta) and calculates
the fraction of stellar luminosity hitting the surface. It also
calculates the temperature change accounting for the surrounding
daisies in the world.
'''

import numpy as np
from daisy import Daisy


# Parcel definition
class Parcel(Daisy):

    def _updatetemp(self, temp1, temp2, temp3, temp4):
        '''Updates parcel parameters in the correct order.'''
        temps = np.array([temp1, temp2, temp3, temp4])
        dT = (temps - self.Teff)

        def gaussian(x):
            '''Temperature efficiency relation.'''
            width = np.max(np.abs(x))/2  # Width of Gaussian for each parcel
            return np.exp(-np.power(x, 2.) / (2 * np.power(width, 2.)))

        effs = 1 - gaussian(dT)  # Calculate efficiencies for each side

        self.Teff = self.Teff + np.average(dT*effs)  # Update T_eff

        if self.Teff < 0.0:
            raise ValueError

        return self.Teff

    def update(self, temp1, temp2, temp3, temp4):
        '''Integrates teh parcel one step'''
        h = 0.001

        # Rk4 solver
        self.rk4Solve(0, h, onestep=True)
        self._updatetemp(temp1, temp2, temp3, temp4)
