#!/bin/bash

for x in ./mklInterior/*/;
do
    cd "${x}";
    printf "Making for ${x} Parallel(D) ...";
    make "CFLAGS=-O3  -std=c99  -I/usr/include/malloc/  -xhost -ipo -fma -fopenmp -DPARALLEL_I=1 -I/s/parsons/l/sys/intel/mkl/include/ -L/s/parsons/l/sys/intel/compilers_and_libraries_2019.3.199/linux/mkl/lib/intel64  -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core  -L/s/parsons/l/sys/intel/lib/intel64 -liomp5 -lm"  &> /dev/null;
    mv BlockTMM BlockTMM_parallel_D;
    mv BlockTMM.check BlockTMM_parallel_D.check
    make clean &> /dev/null;
    printf "done.\n";

    printf "Making for ${x} Parallel(I) ...";
    make "CFLAGS=-O3  -std=c99  -I/usr/include/malloc/  -xhost -ipo -fma -fopenmp -DPARALLEL_J=1 -I/s/parsons/l/sys/intel/mkl/include/ -L/s/parsons/l/sys/intel/compilers_and_libraries_2019.3.199/linux/mkl/lib/intel64  -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core  -L/s/parsons/l/sys/intel/lib/intel64 -liomp5 -lm"  &> /dev/null;
    mv BlockTMM BlockTMM_parallel_I;
    mv BlockTMM.check BlockTMM_parallel_I.check
    make clean &> /dev/null;
    printf "done.\n";



    cd ../../;
done;

