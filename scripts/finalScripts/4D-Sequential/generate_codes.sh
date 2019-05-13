#!/bin/bash

for x in ./tiled/*/;
do
    cd "${x}";
    printf "Generating for ${x}...";
    ./compile.sh *.cs &> /dev/null;
    printf "making...";
    cd out;
    make  CC=icc CFLAGS="-O3 -xhost -ipo -fma" &> /dev/null;
    printf "done.\n";
    cd ../../../;
done;
