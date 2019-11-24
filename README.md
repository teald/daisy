# To-do
+ Write a solid README

# Done
+ Fix really low temperature issue
+ Make sure `a_w` and `a_b` never go above one or below zero for stupid
  reasons.
+ Find best value for `q`.
+ Vectorize daisies and their intrinsic albedos in `Daisy().__init__()`
+ Generalize `Daisy` to take N types of daisies.
+ Make the autostop stopping mechanism stop based on temperature differences
  *or* daisy differences, whichever is greater. Does that make sense? Should it
  just be one?
