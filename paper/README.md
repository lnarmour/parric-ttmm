This directory is self contained with everything needed to run the final experiments for the paper and collect the results.
Specifically, we need to do the following: 

Explore how the following parameters affect performance:
* problem size (N)
* tiling and tile sizes
* loop permutations (6 with non-tiled, more with tiling, etc.)
* data layout: 2D vs. 4D

Want to explore the above parameters for:
* our AlphaZ generated codes
* existing libraries (MKL, BLAS, ATLAS, etc)

For all of the above, we want to gather data on different classes of department machines:
* fish machines (6 cores)
* planet machines (8 cores)
* others, if time permits

For each TMM call (both our code and existing libraries)
* store the machine where it was run
* run 5 times, throw out the top/bottom extremes and average the remaining
* calculate standard deviations
* our current scripts do this mostly but may need some slight tweaking

Report the best performing instances from both our code and existing libraries.