
CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_I=1";

#!/bin/bash

for x in ./nonTiled/*/;
do
    cd "${x}";
    printf "Compiling for ${x} Parallel(I) ...";
    cd out;
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_I=1" &> /dev/null;
    mv TMM TMM_parallel_I;
    make clean;
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_J=1" &> /dev/null;
    mv TMM TMM_parallel_J;
    make clean;
    cd ../../../;
done;

for x in ./tiled/*/;
do
      cd "${x}";
    printf "Compiling for ${x} Parallel(I) ...";
    cd out;
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_I=1" &> /dev/null;
    mv TMM TMM_parallel_I;
    make clean;
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_J=1" &> /dev/null;
    mv TMM TMM_parallel_J;
    make clean;
    cd ../../../;
done;