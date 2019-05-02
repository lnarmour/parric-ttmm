#!/bin/bash
# Return to commit 80fe70e51f4a9d00255958ba0f4894f6170f5962  if you accidentally overwrite hard coded pragmas

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
