for x in firstLoop secndLoop thirdLoop; do  cd $x && make CC=icc CFLAGS="-O3 -xhost -ipo -fma -qopenmp"; cd ..; done
