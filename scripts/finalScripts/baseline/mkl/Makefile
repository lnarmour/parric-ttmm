LIBRARIES=-lm
CC=icc
LD=xild
AR=xiar
MKL_FLAGS=-I/s/parsons/l/sys/intel/mkl/include/ -L/s/chopin/l/grad/lnarmour/parric-shared/intel/compilers_and_libraries/linux/mkl/lib/intel64  -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core  -L/s/chopin/l/grad/lnarmour/parric-shared/intel/compilers_and_libraries/linux/lib/intel64 -liomp5 -lm

CFLAGS=  -std=c99  -I/usr/include/malloc/ $(MKL_FLAGS) -fopenmp -O3
all: ss tt ts

debug: CFLAGS =-DDEBUG -g -Wall -Wextra -std=c99 -I/usr/include/malloc/
debug: all
		
ss:
	$(CC) ss-wrapper.c ss-mkl.c -o SS_MKL $(CFLAGS) $(LIBRARIES)

tt:
	$(CC) tt-wrapper.c ts-mkl.c -o TT_MKL $(CFLAGS) $(LIBRARIES)

ts:
	$(CC) ts-wrapper.c ts-mkl.c -o TS_MKL $(CFLAGS) $(LIBRARIES)

clean:
	rm -f *.o SS_MKL TT_MKL
