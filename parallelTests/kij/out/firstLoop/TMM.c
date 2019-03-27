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


int N;

float ** initialize_R ( ){
    float * temp = malloc(sizeof(float)*(N+1)*(N+1));
    float ** new_R = malloc(sizeof(float*)*(N+1));
    for(int i = 0; i < N+1; i++){
        new_R[i]=temp+(N+1)*i;
        for(int j = 0; j < N+1; j++){
            temp[i*(N+1)+j] = 0;
        }
    }
    return new_R;
}

void combine_R( float ** omp_in, float ** omp_out){
    for (int i = 0; i <= N; i++)
        for (int j = i; j <= N; j++)
            omp_out[i][j] += omp_in[i][j];
    free(omp_in[0]);
    free(omp_in);
}





//Memory Macros
#define A(i,j) A[i][j]
#define B(i,j) B[i][j]
#define R(i,j) R[i][j]

void TMM(long newN, long ts1_l1, long ts2_l1, long ts3_l1, float** A, float** B, float** R){
	N=newN;
    omp_set_num_threads(6);
	///Parameter checking
	if (!((N >= 1 && ts1_l1 > 0 && ts2_l1 > 0 && ts3_l1 > 0))) {
		printf("The value of parameters are not valid.\n");
		exit(-1);
	}
	//Memory Allocation
	
	#define S1(i,j,k) R(j,k) = (R(j,k))+((A(j,i))*(B(i,k)))
	#define S2(i,j,k) R(j,k) = (A(j,i))*(B(i,k))
	#define S0(i,j,i2) R(i,i2) = R(i,i2)
	{
		//Domain
		//{i,j,k|j>=1 && N>=k && k>=i && i>=j+1 && i>=2 && N>=i && k>=j && k>=1 && N>=1}
		//{i,j,k|j==i && i>=1 && N>=k && k>=i && k>=1 && N>=i && N>=1}
		//{i,j,i2|j==N && i2>=1 && N>=i2 && i>=1 && i2>=i && N>=1}
		int ti1_l1,ti2_l1,ti3_l1,c1,c2,c3;
		#pragma omp declare reduction (+:\
                 float** : combine_R(omp_in,omp_out) ) \
                initializer (omp_priv = initialize_R())

            #pragma omp parallel for reduction(+:R)
		for(ti1_l1=(ceild((-ts1_l1+2),(ts1_l1))) * (ts1_l1);ti1_l1 <= N;ti1_l1+=ts1_l1)
		 {
		 	for(ti2_l1=(ceild((-ts2_l1+2),(ts2_l1))) * (ts2_l1);ti2_l1 <= N;ti2_l1+=ts2_l1)
		 	 {
		 	 	for(ti3_l1=(ceild((min(ti1_l1,1) + -ts3_l1+1),(ts3_l1))) * (ts3_l1);ti3_l1 <= N;ti3_l1+=ts3_l1)
		 	 	 {
		 	 	 	{
		 	 	 		for(c1=max(ti1_l1,1);c1 <= min(ti1_l1+ts1_l1-1,1);c1+=1)
		 	 	 		 {
		 	 	 		 	for(c2=max(ti2_l1,1);c2 <= min(ti2_l1+ts2_l1-1,1);c2+=1)
		 	 	 		 	 {
		 	 	 		 	 	for(c3=max(ti3_l1,1);c3 <= min(ti3_l1+ts3_l1-1,N);c3+=1)
		 	 	 		 	 	 {
		 	 	 		 	 	 	S2((1),(1),(c3));
		 	 	 		 	 	 }
		 	 	 		 	 }
		 	 	 		 	for(c2=max(ti2_l1,N);c2 <= min(ti2_l1+ts2_l1-1,N);c2+=1)
		 	 	 		 	 {
		 	 	 		 	 	for(c3=max(ti3_l1,1);c3 <= min(ti3_l1+ts3_l1-1,N);c3+=1)
		 	 	 		 	 	 {
		 	 	 		 	 	 	S0((1),(N),(c3));
		 	 	 		 	 	 }
		 	 	 		 	 }
		 	 	 		 }
		 	 	 		for(c1=max(ti1_l1,2);c1 <= min(ti1_l1+ts1_l1-1,N);c1+=1)
		 	 	 		 {
		 	 	 		 	for(c2=max(ti2_l1,1);c2 <= min(ti2_l1+ts2_l1-1,c1-1);c2+=1)
		 	 	 		 	 {
		 	 	 		 	 	for(c3=max(ti3_l1,c1);c3 <= min(ti3_l1+ts3_l1-1,N);c3+=1)
		 	 	 		 	 	 {
		 	 	 		 	 	 	S1((c1),(c2),(c3));
		 	 	 		 	 	 }
		 	 	 		 	 }
		 	 	 		 	for(c2=max(ti2_l1,c1);c2 <= min(ti2_l1+ts2_l1-1,c1);c2+=1)
		 	 	 		 	 {
		 	 	 		 	 	for(c3=max(ti3_l1,c1);c3 <= min(ti3_l1+ts3_l1-1,N);c3+=1)
		 	 	 		 	 	 {
		 	 	 		 	 	 	S2((c1),(c1),(c3));
		 	 	 		 	 	 }
		 	 	 		 	 }
		 	 	 		 	for(c2=max(ti2_l1,N);c2 <= min(ti2_l1+ts2_l1-1,N);c2+=1)
		 	 	 		 	 {
		 	 	 		 	 	for(c3=max(ti3_l1,c1);c3 <= min(ti3_l1+ts3_l1-1,N);c3+=1)
		 	 	 		 	 	 {
		 	 	 		 	 	 	S0((c1),(N),(c3));
		 	 	 		 	 	 }
		 	 	 		 	 }
		 	 	 		 }
		 	 	 	}
		 	 	 }
		 	 }
		 }
	}
	#undef S1
	#undef S2
	#undef S0
	
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
