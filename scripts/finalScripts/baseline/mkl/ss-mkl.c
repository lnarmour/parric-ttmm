#include <mkl.h>
#include <stdio.h>

void MKLMM(long N, float* A, float* B, float* R){

  cblas_sgemm(CblasRowMajor, //storage format: row major
    CblasNoTrans, //use A, not A transpose
    CblasNoTrans, //Use B, not B transpose
    N, //rows in A
    N, //columns in B
    N, //columns in A/rows in B
    1, //multiply A by 1
    A, 
    N, //leading dimension of A
    B, 
    N, //leading dimension of B
    1, //multiply C by this before adding AB
    R, 
    N);//leading dimension of C

}
