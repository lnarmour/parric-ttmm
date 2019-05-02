
CC=icc CFLAGS="-O3 -xhost -ipo -fma -fopenmp";
make CC=icc CFLAGS="-O3 -xhost -ipo -fma -qopenmp -DPARALLEL_I=1 -L/s/parsons/l/sys/intel/lib/intel64 -liomp5 -lm"
MKL_FLAGS=-I/s/parsons/l/sys/intel/mkl/include/ -L/s/parsons/l/sys/intel/compilers_and_libraries_2018.0.128/linux/mkl/lib/intel64  -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core  -L/s/parsons/l/sys/intel/lib/intel64 -liomp5 -lm
