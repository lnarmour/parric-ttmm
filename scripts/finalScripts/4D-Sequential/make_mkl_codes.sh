#!/bin/bash


for x in ./mklInterior/*/;
do
    cd "${x}";
    printf "Making ${x}...";
    make &> /dev/null;
    printf "done.\n";
    cd ../../;
done;
