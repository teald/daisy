'''
This file defines the TUBE.

Bow down to the TUBE and it may show mercy upon your soul.
'''
# Imports
import numpy as np
import matplotlib.pyplot as plt
import os

import constants as c
from daisy import Daisy
from parcel import Parcel


# Tube definition
class Tube(object):
    '''
    This contains the Tube class.
    '''

    def __init__(self, P, gamma, a_vec, A_vec, phi, T_vec=None):
        self.P = P
        self.gamma = gamma
        self.a_vec = a_vec
        self.A_vec = A_vec
        self.T_vec = T_vec
        self.phi = phi

    def setupGrid(self, n, m, maxtheta):
        self.n = n  # width
        self.m = m  # height
        self.maxtheta = maxtheta  # max latitude to use
        self.deltheta = self.maxtheta / (0.5 * m)  # theta resolution
        self.npix = n * m
        self.thetas = (np.ones([m, n]) * np.linspace(maxtheta, -maxtheta, m)
                       [:, np.newaxis])
        self.Ls = abs(np.sin((90 - self.thetas.reshape(self.npix)) * np.pi/180 + self.phi))

        grid = []
        for i in range(m * n):
            grid.append(Parcel(self.P, self.gamma, self.a_vec, self.A_vec,
                               self.Ls[i], T_vec=self.T_vec))
        self.grid = np.reshape(grid, (m, n))

    def _updategrid(self):
        '''
        Update Parcel parameters for grid.
        '''
        Temps = np.empty([self.m, self.n])

        for m in range(len(self.grid[:, 0])):
            for n in range(len(self.grid[0, :])):  # Go left to right (West to East)
                # Change to for loop with arrays
                if m == 0:
                    T_t = self.grid[m, n].Teff
                else:
                    T_t = self.grid[m-1, n].Teff
                if m == len(self.grid[:, n]) - 1:
                    T_b = self.grid[m, n].Teff
                else:
                    T_b = self.grid[m+1, n].Teff
                if n == 0:
                    T_l = self.grid[m, -1].Teff
                else:
                    T_l = self.grid[m, n-1].Teff
                if n == len(self.grid[m, :]) - 1:
                    T_r = self.grid[m, 0].Teff
                else:
                    T_r = self.grid[m, n+1].Teff

                self.grid[m, n].update(T_t, T_b, T_l, T_r)

                Temps[m, n] = self.grid[m,n].Teff

        if os.path.exists("./output.txt") == True:
            os.remove("./output.txt")

        f = open("output.txt", "a")
        np.savetxt(f, Temps)
        f.close()

    def plot(self, title=""):
        # Plot the grid
        temps = np.genfromtxt("output.txt")[-self.m:]
        plt.imshow(temps, extent=[0, 360, -self.maxtheta, self.maxtheta])
        plt.colorbar()
        plt.clim(240, 320)
        plt.title(title)
        plt.xlabel("Longitude [deg]")
        plt.ylabel("Latitude [deg]")
        plt.grid(b=False)
