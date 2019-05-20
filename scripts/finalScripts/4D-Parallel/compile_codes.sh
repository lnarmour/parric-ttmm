#!/bin/bash

for x in ./tiled/*/;
do
    cd "${x}";
    printf "Compiling for ${x} Parallel(I) ...";
    cd out;
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_I=1" &> /dev/null;
    mv BlockTTMM BlockTTMM_parallel_I;
    mv BlockTTMM.check BlockTTMM_parallel_I.check;
    make clean &> /dev/null;
    printf "done.\n";

    printf "Compiling for ${x} Parallel(J) ...";
    make CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp -DPARALLEL_J=1" &> /dev/null;
    mv BlockTTMM BlockTTMM_parallel_J;
    mv BlockTTMM.check BlockTTMM_parallel_J.check;
    make clean &> /dev/null;
    cd ../../../;
    printf "done.\n";
done;