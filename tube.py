'''
This file defines the TUBE.

Bow down to the TUBE and it may show mercy upon your soul.
'''
# Imports
import pdb
import numpy as np
import matplotlib.pyplot as plt
import os

import constants as c
from daisy import Daisy
from parcel import Parcel
from ocean import Ocean


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

    def read_lands(self, filename):
        '''Reads ina filename that contains some ascii text (o's and x's) that
        have o's representing landmasses and x's representing oceans.'''
        self.maps = []
        with open(filename, 'r') as infile:
            # Checks for compatability
            assert len(infile.lines()), (f"{infile} must have dimensions of"
                                         f"{self.n, self.m}")

            lines = inflie.readlines()

        for line in lines:
            row = []
            for i, l in enumerate(line.split()):
                if l.lower() == 'x':
                    row.append(0)
                elif l.lower() in ['o', 0, '0']:
                    row.append(1)
            self.maps.append(row)


    def setupGrid(self, n, m, maxtheta=80, oceans=False, inputfile=None):
        '''
        Sets up the Tube's grid of parcels.

        Args:
            + n, m (ints): the width and height of the grid. If inputfile is
                provided, the input will be padded to match n and m if one is
                greater than the provided dimensions, and if n and m are less
                than the provided dimensions they will be ignored.
            + maxtheta (float): the maximum latitude (in degrees) to model to.
                Default is 80.
            + oceans (bool): if True, will model oceans (default False). If
                inputfile is provided, will read that in for the oceans (where
                O's are considered oceans, X's landmasses, and spaces are
                ignored.)

                For example, if I had the file:
                    x x o
                    o x x
                    o o o
                This would generate a 3x3 grid (provided n, m are equal to or
                less than 3) with one landmass in cells (0,0), (0,1), (1,1),
                and (1,2), with all other cells filled by oceans.

                If m or n was larger than 3, the remaining cells would be
                padded *by ocean objects*.
            + inputfile (str or None): if None (default) will randomly generate
                oceans if oceans is True. If a string, will use that file per
                the description above to generate a world.

                NOTE: If inputfile is provided, it will override the value of
                oceans and will assume oceans are to be generated.
        '''
        # Read in the inputfile if provided.
        if inputfile is not None:
            # Make sure inputfile is a string
            assert isinstance(inputfile, str), "Infile must be None or" \
                                               "a string"

            # Read in the file
            with open(inputfile, 'r') as infile:
                m = 0
                lines = []

                # Doing it this way for ease of coding, not expensive anyways
                for line in infile.readlines():
                    m += 1
                    n = 0
                    for char in line.strip().split():
                        if char.lower().strip() == 'x':
                            val = 1
                        else:
                            val = 0

                        lines.append(val)
                        n += 1

            landgrid = np.array(lines)

        elif oceans:
            # Randomly generate ocean map
            landgrid = np.random.randint(2, size=m * n)

        else:
            labdgrid = np.ones(m * n)

        # Assign attributes
        self.n = n  # width
        self.m = m  # height
        self.maxtheta = maxtheta  # max latitude to use
        self.deltheta = self.maxtheta / (0.5 * m)  # theta resolution
        self.npix = n * m
        self.thetas = (np.ones([m, n]) * np.linspace(maxtheta, -maxtheta, m)
                       [:, np.newaxis])
        self.Ls = abs(np.sin((90 - self.thetas.reshape(self.npix)) * np.pi/180
                      + self.phi))

        grid = []
        for i, val in enumerate(landgrid):
            if landgrid[i] == 1:
                grid.append(Parcel(self.P, self.gamma, self.a_vec, self.A_vec,
                               self.Ls[i], T_vec=self.T_vec))

            else:
                grid.append(Ocean(290))

        self.grid = np.reshape(grid, (m, n))

    def _updategrid(self):
        '''
        Update Parcel parameters for grid.
        '''
        Temps = np.empty([self.m, self.n])

        for m in range(len(self.grid[:, 0])):
            # Proceed from left to right
            for n in range(len(self.grid[0, :])):
                # Change to for loop with arrays
                # Top
                if m == 0:
                    T_t = self.grid[m, n].Teff
                else:
                    T_t = self.grid[m-1, n].Teff

                # Bottom
                if m == len(self.grid[:, n]) - 1:
                    T_b = self.grid[m, n].Teff
                else:
                    T_b = self.grid[m+1, n].Teff

                # Left
                if n == 0:
                    T_l = self.grid[m, -1].Teff
                else:
                    T_l = self.grid[m, n-1].Teff

                # Right
                if n == len(self.grid[m, :]) - 1:
                    T_r = self.grid[m, 0].Teff
                else:
                    T_r = self.grid[m, n+1].Teff

                self.grid[m, n].update(T_t, T_b, T_l, T_r)

                Temps[m, n] = self.grid[m, n].Teff

        if os.path.exists("./output.txt") == True:
            os.remove("./output.txt")

        f = open("output.txt", "a")
        np.savetxt(f, Temps)
        f.close()


    def plot(self, title="", ptype="Temperature", savefig=None):
        '''
        Plots the grid.

        Args:
            + title (str): Title fo the plot. Default ''.
            + ptype (str): The type of plot to make, default "Temperature". The
                input string is *not* case sensitive!

                Options:
                    - "Temperature"
                    - "Albedo"
                    - "Pops" or "Populations"

            + savefig (string or None): if a string, saves the figure to that
                location. If None, does nothing (should display if the user
                calls plt.show() after this method.
        '''
        plt.figure()
        ptype = ptype.lower()

        if ptype == "temperature":
            # Plot the grid
            temps = []
            only_parcels = []
            for row in self.grid:
                temprow = []
                for area in row:
                    temprow.append(area.Teff)

                    if isinstance(area, Parcel):
                        only_parcels.append(area.Teff)

                temps.append(temprow)

            plt.imshow(temps, extent=[0, 360, -self.maxtheta, self.maxtheta],
                       aspect='equal')
            plt.colorbar()
            plt.clim(240, 320)
            plt.clim(np.amin(only_parcels), np.amax(only_parcels))
            plt.title(title)
            plt.xlabel("Longitude [deg]")
            plt.ylabel("Latitude [deg]")
            plt.grid(b=False)

        elif ptype == "albedo":
            # Plot the grid
            albedos = []
            only_parcels = []

            for row in self.grid:
                temprow = []

                for area in row:
                    temprow.append(area.A)

                    # Get parcels only for the colorbar
                    if isinstance(area, Parcel):
                        only_parcels.append(area.A)
                albedos.append(temprow)

            plt.imshow(albedos, extent=[0, 360, -self.maxtheta, self.maxtheta],
                       aspect='equal', cmap='gray')
            plt.colorbar()
            plt.clim(np.amin(only_parcels), np.amax(only_parcels))
            plt.title(title)
            plt.xlabel("Longitude [deg]")
            plt.ylabel("Latitude [deg]")
            plt.grid(b=False)

        elif ptype in ['pops', 'population']:
            # Plot the grid
            pops = []
            only_parcels = []

            for row in self.grid:
                temprow = []

                for area in row:
                    # Get parcels to get pops and for colorbar not including
                    # the ground.
                    if isinstance(area, Parcel):
                        only_parcels.append(np.sum(area.a_vec[:-1]))
                        temprow.append(np.sum(area.a_vec[:-1]))

                    else:
                        temprow.append(0.)
                pops.append(temprow)

            plt.imshow(pops, extent=[0, 360, -self.maxtheta, self.maxtheta],
                       aspect='equal', cmap='gray')
            plt.colorbar()
            plt.clim(np.amin(only_parcels), np.amax(only_parcels))
            plt.title(title)
            plt.xlabel("Longitude [deg]")
            plt.ylabel("Latitude [deg]")
            plt.grid(b=False)

        elif ptype in [str(_d) for _d in range(len(self.a_vec))]:
            # Plot the grid
            pops = []
            only_parcels = []

            for row in self.grid:
                temprow = []

                for area in row:
                    # Get parcels to get pops and for colorbar not including
                    # the ground.
                    if isinstance(area, Parcel):
                        only_parcels.append(np.sum(area.a_vec[int(ptype)]))
                        temprow.append(np.sum(area.a_vec[int(ptype)]))

                    else:
                        temprow.append(0.)
                pops.append(temprow)

            plt.imshow(pops, extent=[0, 360, -self.maxtheta, self.maxtheta],
                       aspect='equal', cmap='gray')
            plt.colorbar()
            plt.clim(np.amin(only_parcels), np.amax(only_parcels))
            plt.title(title)
            plt.xlabel("Longitude [deg]")
            plt.ylabel("Latitude [deg]")
            plt.grid(b=False)


        else:
            # Incorrect plot type passed
            raise ValueError("Unrecognized ptype passed. Please select from"
                             " the options listed in the documentation.")

        if savefig is not None:
            # Save the figure
            plt.gcf().savefig(savefig)
            plt.close(plt.gcf())
