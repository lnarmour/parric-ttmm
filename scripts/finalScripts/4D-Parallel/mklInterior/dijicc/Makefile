LIBRARIES=-lm
CC=icc
LD=xild
AR=xiar
OBJS = BlockTTMM.o 
MKL_FLAGS=-I/s/parsons/l/sys/intel/mkl/include/ -L/s/parsons/l/sys/intel/compilers_and_libraries_2019.3.199/linux/mkl/lib/intel64  -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core  -L/s/parsons/l/sys/intel/lib/intel64 -liomp5 -lm
CFLAGS=  -O3  -std=c99  -I/usr/include/malloc/ -xhost -ipo -fma -fopenmp -DPARALLEL_J=1 $(MKL_FLAGS)
all: plain check

debug: CFLAGS =-DDEBUG -g -Wall -Wextra -std=c99 -I/usr/include/malloc/
debug: all
		
plain: $(OBJS)
	$(CC) BlockTTMM-wrapper.c -o BlockTTMM $(OBJS) $(CFLAGS) $(LIBRARIES)

check: $(OBJS)
	$(CC) BlockTTMM-wrapper.c -o BlockTTMM.check $(OBJS) $(CFLAGS) $(LIBRARIES) -DCHECKING

verify: $(OBJS) BlockTTMM_verify.o
	$(CC) BlockTTMM-wrapper.c -o BlockTTMM.verify $(OBJS) BlockTTMM_verify.o $(CFLAGS) $(LIBRARIES) -DVERIFY

verify-rand: $(OBJS) BlockTTMM_verify.o
	$(CC) BlockTTMM-wrapper.c -o BlockTTMM.verify-rand $(OBJS) BlockTTMM_verify.o $(CFLAGS) $(LIBRARIES) -DVERIFY -DRANDOM

BlockTTMM.o : BlockTTMM.c
	$(CC) BlockTTMM.c -o BlockTTMM.o $(CFLAGS) $(LIBRARIES) -c

BlockTTMM_verify.o : BlockTTMM_verify.c
	$(CC) BlockTTMM_verify.c -o BlockTTMM_verify.o $(CFLAGS) $(LIBRARIES) -c

clean:
	rm -f *.o BlockTTMM BlockTTMM.check BlockTTMM.verify BlockTTMM.verify-rand
