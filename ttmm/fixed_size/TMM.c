// This file is generated from test alphabets program by code generator in alphaz
// To compile this code, use -lm option for math library.

// Includes
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <limits.h>
#include <float.h>
#include <omp.h>
#include <immintrin.h>
#include <malloc.h>
#include <mkl.h>
#include "blockformat.h"
#include <string.h>

// Common Macros
#define max(x, y)   ((x)>(y) ? (x) : (y))
#define MAX(x, y)	((x)>(y) ? (x) : (y))
#define min(x, y)   ((x)>(y) ? (y) : (x))
#define MIN(x, y)	((x)>(y) ? (y) : (x))
#define CEILD(n,d)  (int)ceil(((double)(n))/((double)(d)))
#define ceild(n,d)  (int)ceil(((double)(n))/((double)(d)))
#define FLOORD(n,d) (int)floor(((double)(n))/((double)(d)))
#define floord(n,d) (int)floor(((double)(n))/((double)(d)))
#define CDIV(x,y)    CEILD((x),(y))
#define div(x,y)    CDIV((x),(y))
#define FDIV(x,y)    FLOORD((x),(y))
#define LB_SHIFT(b,s)  ((int)ceild(b,s) * s)
#define MOD(i,j)   ((i)%(j))
#define mallocCheck(v,s,d) if ((v) == NULL) { printf("Failed to allocate memory for %s : size=%lu\n", "sizeof(d)*(s)", sizeof(d)*(s)); exit(-1); }
// Reduction Operators
#define RADD(x,y)    ((x)+=(y))
#define RMUL(x,y)    ((x)*=(y))
#define RMAX(x,y)    ((x)=MAX((x),(y)))
#define RMIN(x,y)    ((x)=MIN((x),(y)))

// Common functions for min and max
//functions for integer max
inline int __max_int(int x, int y){
	return ((x)>(y) ? (x) : (y));
}

inline short __max_short(short x, short y){
	return ((x)>(y) ? (x) : (y));
}

inline long __max_long(long x, long y){
	return ((x)>(y) ? (x) : (y));
}

inline unsigned int __max_unsigned_int(unsigned int x, unsigned int y){
	return ((x)>(y) ? (x) : (y));
}

inline unsigned short __max_unsigned_short(unsigned short x, unsigned short y){
	return ((x)>(y) ? (x) : (y));
}

//function for float max
inline float __max_float(float x, float y){
	return ((x)>(y) ? (x) : (y));
}

//function for double max
inline double __max_double(double x, double y){
	return ((x)>(y) ? (x) : (y));
}

//function for integer min
inline int __min_int(int x, int y){
	return ((x)>(y) ? (y) : (x));
}

inline short __min_short(short x, short y){
	return ((x)>(y) ? (y) : (x));
}

inline long __min_long(long x, long y){
	return ((x)>(y) ? (y) : (x));
}

inline unsigned int __min_unsigned_int(unsigned int x, unsigned int y){
	return ((x)>(y) ? (y) : (x));
}

inline unsigned short __min_unsigned_short(unsigned short x, unsigned short y){
	return ((x)>(y) ? (y) : (x));
}

inline unsigned long __min_unsigned_long(unsigned long x, unsigned long y){
	return ((x)>(y) ? (y) : (x));
}

inline float __min_float(float x, float y){
	return ((x)>(y) ? (y) : (x));
}

inline double __min_double(double x, double y){
	return ((x)>(y) ? (y) : (x));
}





//Memory Macros
#define A(i,j) A[i][j]
#define B(i,j) B[i][j]
#define R(i,j) R[i][j]

void TMM(long N, long ts1_l1, long ts2_l1, long ts3_l1, float** A, float** B, float** R){
	///Parameter checking
	if (!((N >= 1 && ts1_l1 > 0 && ts2_l1 > 0 && ts3_l1 > 0))) {
		printf("The value of parameters are not valid.\n");
		exit(-1);
	}
        //clear R
        memset(R[0], 0, sizeof(float)*(N+1)*(N+1));
	//Memory Allocation
	
	#define S1(i,j,k) R(i,k) = (A(i,j))*(B(j,k))
	#define S2(i,j,k) R(i,k) = (R(i,k))+((A(i,j))*(B(j,k)))
	#define S0(i,j,i2) R(i,i2) = R(i,i2)
	//wrapper allocates matrices contiguously, so first row pointer works as pointer for entire matrix
	float *flatA=A[0], *flatB=B[0], *flatC=R[0];
    //bm is block-major
    float *bmA, *bmB, *bmC;
    int new_sizeA=0;
    bmA=toBlocks(flatA,N+1, &new_sizeA);
    int new_sizeB=0;
    bmB=toBlocks(flatB,N+1, &new_sizeB);
    int new_sizeC=0;
    bmC=toBlocks(flatC,N+1, &new_sizeC);
    
	{
		for(int i=0;i<new_sizeA/SIZE;i++)
            for(int j=i;j<new_sizeB/SIZE;j++)
                for(int k=i;k<=j;k++)
                    cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, SIZE, SIZE, SIZE, 1, bmA+(i*SIZE*new_sizeA+k*SIZE), SIZE, bmB+(k*SIZE*new_sizeB+j*SIZE), SIZE, 1, bmC+(i*SIZE*new_sizeC+j*SIZE), SIZE);
                
	}
	#undef S1
	#undef S2
	#undef S0
    //copy from bmC to R
    fromBlocks(bmC, flatC, new_sizeC, N+1);
	//Memory Free
}

//Memory Macros
#undef A
#undef B
#undef R


//Common Macro undefs
#undef max
#undef MAX
#undef min
#undef MIN
#undef CEILD
#undef ceild
#undef FLOORD
#undef floord
#undef CDIV
#undef FDIV
#undef LB_SHIFT
#undef MOD
#undef RADD
#undef RMUL
#undef RMAX
#undef RMIN