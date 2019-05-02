#!/bin/bash

ECLIPSE=/s/chopin/e/proj/AlphaZ/BinTree/eclipse-alphaz-bundle/eclipse/eclipse

SCRIPT="$1"

${ECLIPSE} -application fr.irisa.r2d2.gecos.framework.compiler -c ${SCRIPT} -data /tmp -noSplash

rm -rf .jnimap.temp.linux_64 *.glog
