#include <mkl.h>
#include <stdio.h>

void MKLMM(long N, float* A, float* B){

  cblas_strmm(CblasRowMajor, //storage format: row major
		CblasLeft, // order in which matrices should be multiplied
		CblasUpper, // upper triangular
		CblasNoTrans,
		CblasNonUnit, // not unit-triangular
		N, // rows in B
		N, // cols in B
		1, // scaling factor for A
		A, // triangular matrix
		N, // leading dimension of A
		B, // matrix B
    N); // leading dimension of B

		// B is OVERWRITTEN during this cblas_trmm

}
