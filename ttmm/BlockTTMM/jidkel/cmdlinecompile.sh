#!/bin/bash

# if this is running in the docker 'slave' container then eclipse will be located at /home/jenkins/eclipse/
if [[ -e /home/jenkins/eclipse/eclipse ]];
then
    ECLIPSE=/home/jenkins/eclipse/eclipse
else
    ECLIPSE=/s/chopin/e/proj/AlphaZ/BinTree/eclipse-alphaz-bundle/eclipse/eclipse
fi

SCRIPT=jidkel.cs
WORKSPACE=./..

${ECLIPSE} -application fr.irisa.r2d2.gecos.framework.compiler -c ${SCRIPT} -data ${WORKSPACE} -noSplash
