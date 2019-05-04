#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

void MKLMM(long, float*, float*, float*);

int main(int argc, char** argv) {
  //Check number of args
  if (argc <= 1) {
    printf("Number of argument is smaller than expected.\n");
    printf("Expecting N\n");
    exit(0);
  }

  int N = atoi(argv[1]);

	//Timing
	struct timeval time;
	double elapsed_time;

	float *A = malloc(N * N * sizeof(float));
	float *B = malloc(N * N * sizeof(float));
	float *C = malloc(N * N * sizeof(float));

	for (long i=0; i<N; i++)
		for (long j=0; j<N; j++) {
			*(A+i*N+j) = 1.14;
			*(B+i*N+j) = 1.14;
		}

  //Call the main computation
  gettimeofday(&time, NULL);
  elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000);

	MKLMM(N, A, B, C);

  gettimeofday(&time, NULL);
  elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000) - elapsed_time;

  // timing information
  //printf("Execution time : %lf sec.\n", elapsed_time);

  printf("Execution time : %lf sec.\n", elapsed_time);







	if (0==1) {
  	for (long i=0; i<N; i++) {
  	  for (long j=0; j<N; j++) {
  	    printf("%f  ", *(A+i*N+j));
  	  }
  	  printf("\n");
  	}
		printf("\n");

  	for (long i=0; i<N; i++) {
  	  for (long j=0; j<N; j++) {
  	    printf("%f  ", *(B+i*N+j));
  	  }
  	  printf("\n");
  	}
		printf("\n");


		for (long i=0; i<N; i++) {
		  for (long j=0; j<N; j++) {
				printf("%f  ", *(C+i*N+j));
		  }
			printf("\n");
		}
	}
		

}
