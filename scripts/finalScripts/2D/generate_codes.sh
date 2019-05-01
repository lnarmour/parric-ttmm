#!/bin/bash

for x in ./nonTiled/*/;
do
    cd "${x}";
    printf "Generating for ${x}...";
    ./compile.sh TMMScript.cs &> /dev/null;
    printf "done.\n";
    cd ../../;
done;
