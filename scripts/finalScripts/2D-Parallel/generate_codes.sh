#!/bin/bash

for x in ./nonTiled/*/;
do
    cd "${x}";
    printf "Generating for ${x}...";
    # not meant be run
    # here for historical purposes
    #./compile.sh TMMScript.cs &> /dev/null;
    printf "making...";
    cd out;
    make &> /dev/null;
    printf "done.\n";
    cd ../../../;
done;

for x in ./tiled/*/;
do
    cd "${x}";
    printf "Generating for ${x}...";
    # not meant be run
    # here for historical purposes
    #./compile.sh TMMScript.cs &> /dev/null;
    printf "making...";
    cd out;
    make &> /dev/null;
    printf "done.\n";
    cd ../../../;
done;
