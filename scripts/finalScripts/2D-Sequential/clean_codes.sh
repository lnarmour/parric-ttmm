#!/bin/bash

for x in ./nonTiled/*/;
do
    cd "${x}";
    printf "Cleaning ${x}...";
    ./compile.sh TMMScript.cs &> /dev/null;
    rm -r out/;
    printf "done.\n";
    cd ../../;
done;

for x in ./tiled/*/;
do
    cd "${x}";
    printf "Cleaning ${x}...";
    ./compile.sh TMMScript.cs &> /dev/null;
    rm -r out/;
    printf "done.\n";
    cd ../../;
done;