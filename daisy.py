'''
Defines the Daisy class, which models a patch of daisies.

--- Teal (teal@astro.umd.edu)
'''
import numpy as np

class Daisy(object):
    '''
    The Daisy class models a single patch of daisies.
    '''

    def __init__(self):
        '''
        Initializes the Daisy class.

        Args:
            +
        '''
        # Area of the patch
        self.area = 1.

        # Surface albedo (no daisies)
        self.A_surf = 0.5

        # Albedo of a white daisy
        self.A_white = 1.

        # Albedo of a black daisy
        self.A_black = 0.



