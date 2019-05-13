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
#define A(i,j,k,l) A[i][j][k][l]
#define B(i,j,k,l) B[i][j][k][l]
#define C(i,j,k,l) C[i][j][k][l]

void BlockTTMM(long n, long b, float**** A, float**** B, float**** C){
	///Parameter checking
	if (!((n >= 1 && b >= 1))) {
		printf("The value of parameters are not valid.\n");
		exit(-1);
	}
	//Memory Allocation
	
	#define S1(i,j,k,l,i4,i5) C(j,k,l,i5) = 0
	#define S0(i,j,k,l,d,e) C(j,k,l,e) = (C(j,k,l,e))+((A(j,i,l,d))*(B(i,k,d,e)))
	{
		//Domain
		//{i,j,k,l,i4,i5|i4==0 && i==0 && n>=1 && b>=1 && j>=0 && k>=j && n>=k+1 && l>=0 && b>=l+1 && i5>=0 && b>=i5+1}
		//{i,j,k,l,d,e|j>=0 && i>=j && n>=i+1 && l>=0 && b>=l+1 && d>=0 && b>=d+1 && n>=1 && b>=1 && i>=0 && k>=i && n>=k+1 && b>=e+1 && e>=0 && k>=j}
		int c1,c2,c3,c4,c5,c6;
		if ((b >= 2 && n >= 2)) {
			{
				for(c3=0;c3 <= n-1;c3+=1)
				 {
				 	for(c4=0;c4 <= b-1;c4+=1)
				 	 {
				 	 	for(c6=0;c6 <= b-1;c6+=1)
				 	 	 {
				 	 	 	S1((0),(0),(c3),(c4),(0),(c6));
				 	 	 	S0((0),(0),(c3),(c4),(0),(c6));
				 	 	 }
				 	 	for(c5=1;c5 <= b-1;c5+=1)
				 	 	 {
				 	 	 	for(c6=0;c6 <= b-1;c6+=1)
				 	 	 	 {
				 	 	 	 	S0((0),(0),(c3),(c4),(c5),(c6));
				 	 	 	 }
				 	 	 }
				 	 }
				 }
				for(c2=1;c2 <= n-1;c2+=1)
				 {
				 	for(c3=c2;c3 <= n-1;c3+=1)
				 	 {
				 	 	for(c4=0;c4 <= b-1;c4+=1)
				 	 	 {
				 	 	 	for(c6=0;c6 <= b-1;c6+=1)
				 	 	 	 {
				 	 	 	 	S1((0),(c2),(c3),(c4),(0),(c6));
				 	 	 	 }
				 	 	 }
				 	 }
				 }
			}
		}
		if ((b >= 2 && n == 1)) {
			{
				for(c4=0;c4 <= b-1;c4+=1)
				 {
				 	for(c6=0;c6 <= b-1;c6+=1)
				 	 {
				 	 	S1((0),(0),(0),(c4),(0),(c6));
				 	 	S0((0),(0),(0),(c4),(0),(c6));
				 	 }
				 	for(c5=1;c5 <= b-1;c5+=1)
				 	 {
				 	 	for(c6=0;c6 <= b-1;c6+=1)
				 	 	 {
				 	 	 	S0((0),(0),(0),(c4),(c5),(c6));
				 	 	 }
				 	 }
				 }
			}
		}
		if ((b == 1 && n >= 2)) {
			{
				for(c3=0;c3 <= n-1;c3+=1)
				 {
				 	S1((0),(0),(c3),(0),(0),(0));
				 	S0((0),(0),(c3),(0),(0),(0));
				 }
				for(c2=1;c2 <= n-1;c2+=1)
				 {
				 	for(c3=c2;c3 <= n-1;c3+=1)
				 	 {
				 	 	S1((0),(c2),(c3),(0),(0),(0));
				 	 }
				 }
			}
		}
		if ((b == 1 && n == 1)) {
			{
				S1((0),(0),(0),(0),(0),(0));
				S0((0),(0),(0),(0),(0),(0));
			}
		}
		for(c1=1;c1 <= n-1;c1+=1)
		 {
		 	for(c2=0;c2 <= c1;c2+=1)
		 	 {
		 	 	for(c3=c1;c3 <= n-1;c3+=1)
		 	 	 {
		 	 	 	for(c4=0;c4 <= b-1;c4+=1)
		 	 	 	 {
		 	 	 	 	for(c5=0;c5 <= b-1;c5+=1)
		 	 	 	 	 {
		 	 	 	 	 	for(c6=0;c6 <= b-1;c6+=1)
		 	 	 	 	 	 {
		 	 	 	 	 	 	S0((c1),(c2),(c3),(c4),(c5),(c6));
		 	 	 	 	 	 }
		 	 	 	 	 }
		 	 	 	 }
		 	 	 }
		 	 }
		 }
	}
	#undef S1
	#undef S0
	
	//Memory Free
}

//Memory Macros
#undef A
#undef B
#undef C


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
