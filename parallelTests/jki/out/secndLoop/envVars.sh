#!/bin/bash

make clean
make all

export OMP_NUM_THREADS=1
./TMM.verify-rand 2000 100 100 100

export OMP_NUM_THREADS=$1
./TMM.verify-rand 2000 100 100 100
