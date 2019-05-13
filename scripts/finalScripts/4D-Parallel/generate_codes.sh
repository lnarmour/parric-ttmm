#!/bin/bash

for x in ./tiled/*/;
do
    # not meant be run
    # here for historical purposes
    cd "${x}";
    printf "Generating for ${x}...";
    #./compile.sh *.cs &> /dev/null;
    printf "done.\n";
    cd ../../;
done;

