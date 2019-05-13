#! /usr/bin/bash
for outer in ijd idj dij dji jid jdi
 do cd ${outer}icc/out/BlockTTMM
 make clean
 make
 cd ../../..
done
