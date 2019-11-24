# `daisy`
`daisy` is a package that simulates the Daisyworld model as proposed by Watson
and Lovelock 1983 for a 2D surface rather than a global surface.

After cloning, make sure to run the following tests:

1. Run `python test_orig.py`. This will run the standard Daisyworld models
   shown in Figure 1 of Watson & Lovelock 1983.
1. Run `python testing_time.py` to ensure that there are no suspicious
   numerical instabilities with your current python setup and machine (this
   step can be skipped if need be, but is a sanity check should bug with
   stabilityarise).

Once this is done, you are ready to play around with all the `daisy` package
has to offer.

## Running Daisyworld simulations (1D)
Running daisyworld simulations, assuming you _do not want any temperature
forcing_, can be done solely through the `Daisy` class. To import the daisy
class, simply us `from daisy import Daisy`. `Daisy` contains many of the
numerical functions used by `Parcel` and `Tube`, so this is a great place to
start for running the suite of models offered.

The test file `test_orig.py` contains a script that will reproduce the original
models run by Watson & Lovelock 1983, and produces the equivalent figures from
their Figure 1. The differences in the generated population values form our
model & that model are attributed to the fact that we do not make the same
assumptions Watson makes (specifically, the linear approximation to Equation 6,
defined by Equation 7).

To run your own simulations, reading the specific docstrings and comments in
`Daisy`'s definition would be ideal. As a brief cheat guide though, we outline
some of those here.

### Initializing a `Daisy` object
To initialize a `Daisy` object, one much be sure to pass in the correct arguments. `Daisy` requires at minimum _4 argumnets_ when an object is created:
+ P (float): the fertile area the daisies have to grow.
+ gamma (float): the death rate of the daisies in daisies/day.
+ a_vec (array): the numpy 1D array containing the fractional area
    covered by each desired species of daisy
+ A_vec (array): the numpy 1D array containing the albedos of each
    daisy species in a_vec

Furthermore, there are `kwargs` with default values typically corresponding to the Watson & Lovelock 1983 values.
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
+ S (float or arr): The solar surface flux in erg/cm^2/s (default
    c.S, from the constants file). If this is an array, effs must
    be an array with the efficiency ranges of the daisies or this
    will be taken as a broad-band flux, and the array should
    contain corresponding wavelengths in Angstroms.
+ q (float or arr): The absorption efficiency of the daisies and
    ground (default c.q).
+ effs (arr or None (Default)): the effs array is used to calculate
    specific daisy color albedos to determine the absorption and
    reflectance of specific daisy species. Should be an array of
    shape (N_daisies, 2) where N_daisies is the number fo daisies
    and each row contains the reflecting wavelengths of the
    daisies.

## To-do
+ Make `test_orig.py` overplot the Watson & Lovelock 1983 results per Derek's request.
+ Write a solid README

## Done
+ Fix really low temperature issue
+ Make sure `a_w` and `a_b` never go above one or below zero for stupid
  reasons.
+ Find best value for `q`.
+ Vectorize daisies and their intrinsic albedos in `Daisy().__init__()`
+ Generalize `Daisy` to take N types of daisies.
+ Make the autostop stopping mechanism stop based on temperature differences
  *or* daisy differences, whichever is greater. Does that make sense? Should it
  just be one?
