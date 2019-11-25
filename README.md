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
To initialize a `Daisy` object, one much be sure to pass in the correct arguments. `Daisy` requires at minimum _4 arguments_ when an object is created:
+ `P` (`float`): the fertile area the daisies have to grow.
+ `gamma` (`float`): the death rate of the daisies in daisies/day.
+ `a_vec` (`array`): the numpy 1D array containing the fractional area
    covered by each desired species of daisy
+ `A_vec` (`array`): the numpy 1D array containing the albedos of each
    daisy species in a_vec

Furthermore, there are `kwargs` with default values typically corresponding to the Watson & Lovelock 1983 values.
+ `L` (`float`): the fraction of solar flux incident on the surface
    (where S = 9.17e5 erg/cm^2/s is the solar flux at Earth's
    surface.
+ `T_vec` (`array` or`None`): the numpy 1D array of optimal temperatures
    for each daise species. If None (default) uses the default
    optimal daisy temperature from Watson & Lovelock 1983.
+ `verbose` (`bool`): if True, prints out A LOT. If False (default) it
    will not do that.
+ `A_g` (`float`): albedo of the ground for the fraction of land not
    covered by daisies. Default 0.5
+ `S` (`float` or `arr`): The solar surface flux in erg/cm^2/s (default
    c.S, from the constants file). If this is an array, effs must
    be an array with the efficiency ranges of the daisies or this
    will be taken as a broad-band flux, and the array should
    contain corresponding wavelengths in Angstroms.
+ `q` (`float` or `arr`): The absorption efficiency of the daisies and
    ground (default c.q).
+ `effs` (`arr` or `None` (Default)): the effs array is used to calculate
    specific daisy color albedos to determine the absorption and
    reflectance of specific daisy species. Should be an array of
    shape (N_daisies, 2) where N_daisies is the number fo daisies
    and each row contains the reflecting wavelengths of the
    daisies.

### Running an integration
This model uses time-integration of the Daisyworld equations to some threshold
of stability. This all happens withing the `Daisy().rk4Solve()` method, which
implements our in-house Pythonic 4th Order Runge-Kutta solver. This method
requires 2 arguments:
+ `maxsteps` (`int`): maximum number of steps to take
+ `h` (float): the time step size to take. The smaller this is, the more
  accurate the integration will be when it finishes.

This will integrate until either `maxsteps` iterations have happened _or_ the temperature and population differences between the previous and current step are less than `1e-4`. After one of those conditions is met, the method returns.

For the purposes of adding additional conditions or, with our `Parcel` and
`Tube` classes, mapping individual `Daisy` objects to a surface, one can use
the `onestep` kwarg. Using `Daisy().rk4Solve(maxstep, h, onestep=True)` will
run only one step of the rk4 integration before returning. This allows for
considitons to be added in between steps of the rk4 solver.

## Parcel object
This object is meant to be a mediator between a Daisy object and all the surrounding Daisy objects. There are two functions
in the Parcel objects.

### _updatetemp
This function takes in the temperatures of the surrounding parcels and calculates the new effective temperature of the
parcel. It calculates the efficiency of temperature transport based on the difference between a surrounding parcel and the
current parcel in question. The efficiencies are drawn from a Gaussian distribution with a width based on the maximum
temperature difference between the parcel in question and the surrounding parcels. It will then update the effective
temperature based on the average of the temperatures of the surrounding parcels attentuated by their efficiency. It takes in the four temperatures from the four surrounding parcels as arguments.

### update
This function simply updates the parameters for the Daisy object within the Parcel object and initializes the next step of the RK4 solver.

## To-do
+ Make `test_orig.py` overplot the Watson & Lovelock 1983 results per Derek's request.
+ Write a solid README
+ Make sure to include a dashed line in a Figure 3 sampling plot to show that these randomly sampled runs all surround the normal no-daisy limit.
+ Make plots look nice

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
