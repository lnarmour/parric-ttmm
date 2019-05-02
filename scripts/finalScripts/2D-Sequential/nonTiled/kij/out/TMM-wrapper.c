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
#include <time.h>
#include <sys/time.h>
#include <sys/errno.h>
#include <omp.h>
#ifdef PAPI
#include <papi.h>
#endif


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
#define EPSILON 1.0E-9







//Memory Macros
#define A(i,j) A[i][j]
#define B(i,j) B[i][j]
#define R(i,j) R[i][j]

#define R_verify(i,j) R_verify[i][j]
#define var_R(i,j) R(i,j)
#define var_R_verify(i,j) R_verify(i,j)

//function prototypes
void TMM(long, float**, float**, float**);
void TMM_verify(long, float**, float**, float**);

//main
int main(int argc, char** argv) {
	//Check number of args
	if (argc <= 1) {
		printf("Number of argument is smaller than expected.\n");
		printf("Expecting N\n");
		exit(0);
	}
	
	char *end = 0;
	char *val = 0;
	//Read Parameters
	//Initialisation of N
	errno = 0;
	end = 0;
	val = argv[1];
	long N = strtol(val,&end,10);
	if ((errno == ERANGE && (N == LONG_MAX || N == LONG_MIN)) || (errno != 0 && N == 0)) {
		perror("strtol");
		exit(EXIT_FAILURE);
	}
	if (end == val) {
		fprintf(stderr, "No digits were found for N\n");
		exit(EXIT_FAILURE);
	}
	if (*end != '\0'){
		printf("For parameter N: Converted part: %ld, non-convertible part: %s\n", N, end);
		exit(EXIT_FAILURE);
	}
	
	
	///Parameter checking
	if (!((N >= 1))) {
		printf("The value of parameters are not valid.\n");
		exit(-1);
	}
	
	
	//Memory Allocation
	int mz1, mz2;
	float* _lin_A = (float*)malloc(sizeof(float)*((N+1) * (N+1)));
	mallocCheck(_lin_A, ((N+1) * (N+1)), float);
	float** A = (float**)malloc(sizeof(float*)*(N+1));
	mallocCheck(A, (N+1), float*);
	for (mz1=0;mz1 < N+1; mz1++) {
		A[mz1] = &_lin_A[(mz1*(N+1))];
	}
	float* _lin_B = (float*)malloc(sizeof(float)*((N+1) * (N+1)));
	mallocCheck(_lin_B, ((N+1) * (N+1)), float);
	float** B = (float**)malloc(sizeof(float*)*(N+1));
	mallocCheck(B, (N+1), float*);
	for (mz1=0;mz1 < N+1; mz1++) {
		B[mz1] = &_lin_B[(mz1*(N+1))];
	}
	float* _lin_R = (float*)malloc(sizeof(float)*((N+1) * (N+1)));
	mallocCheck(_lin_R, ((N+1) * (N+1)), float);
	float** R = (float**)malloc(sizeof(float*)*(N+1));
	mallocCheck(R, (N+1), float*);
	for (mz1=0;mz1 < N+1; mz1++) {
		R[mz1] = &_lin_R[(mz1*(N+1))];
	}
	#ifdef VERIFY
		float* _lin_R_verify = (float*)malloc(sizeof(float)*((N+1) * (N+1)));
		mallocCheck(_lin_R_verify, ((N+1) * (N+1)), float);
		float** R_verify = (float**)malloc(sizeof(float*)*(N+1));
		mallocCheck(R_verify, (N+1), float*);
		for (mz1=0;mz1 < N+1; mz1++) {
			R_verify[mz1] = &_lin_R_verify[(mz1*(N+1))];
		}
	#endif

	//Initialization of rand
	srand((unsigned)time(NULL));
	 
	//Input Initialization
	{
		#if defined (RANDOM)
			#define S0(i,j) (A(i,j) = rand()%8); //fprintf(stderr, "%f\n",A(i,j)); 
		#elif defined (CHECKING) || defined (VERIFY)
			#ifdef NO_PROMPT
				#define S0(i,j) scanf("%f", &A(i,j))
			#else
				#define S0(i,j) printf("A(%ld,%ld)=",(long) i,(long) j); scanf("%f", &A(i,j))
			#endif
		#else
			#define S0(i,j) (A(i,j) = 1)   //Default value
		#endif
		
		
		int c1,c2;
		for(c1=1;c1 <= N;c1+=1)
		 {
		 	for(c2=c1;c2 <= N;c2+=1)
		 	 {
		 	 	S0((c1),(c2));
		 	 }
		 }
		#undef S0
	}
	{
		#if defined (RANDOM)
			#define S0(i,j) (B(i,j) = rand()%8); //fprintf(stderr, "%f\n",B(i,j)); 
		#elif defined (CHECKING) || defined (VERIFY)
			#ifdef NO_PROMPT
				#define S0(i,j) scanf("%f", &B(i,j))
			#else
				#define S0(i,j) printf("B(%ld,%ld)=",(long) i,(long) j); scanf("%f", &B(i,j))
			#endif
		#else
			#define S0(i,j) (B(i,j) = 1)   //Default value
		#endif
		
		
		int c1,c2;
		for(c1=1;c1 <= N;c1+=1)
		 {
		 	for(c2=c1;c2 <= N;c2+=1)
		 	 {
		 	 	S0((c1),(c2));
		 	 }
		 }
		#undef S0
	}
	
	//exit(0);
	
	//Timing
	struct timeval time;
	double elapsed_time;
	
#ifdef PAPI
    int retval, EventSet = PAPI_NULL, native;
    long_long PAPIvalues[5];
    retval = PAPI_library_init(PAPI_VER_CURRENT);

    if (retval != PAPI_VER_CURRENT) {
      fprintf(stderr, "PAPI library init error!\n");
      exit(1);
    }

	int EventCode;
	char EventCodeStr[PAPI_MAX_STR_LEN];

  	EventCode = 0 | PAPI_NATIVE_MASK;
	  
	if (PAPI_create_eventset(&EventSet) != PAPI_OK)
		printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
	if (PAPI_add_event(EventSet, PAPI_TOT_INS) != PAPI_OK)
	    printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
	if (PAPI_add_event(EventSet, PAPI_L3_TCM) != PAPI_OK)
	    printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
	sprintf( EventCodeStr, "OFFCORE_RESPONSE_0:ANY_DATA:LLC_MISS_LOCAL_DRAM" ); 
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_1:ANY_REQUEST:L3_MISS" );   
    //sprintf( EventCodeStr, "OFFCORE_RESPONSE_0:DMND_DATA_RD:L3_MISS" );
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_0:DMND_RFO:L3_MISS" );
	
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_0:PF_LLC_RFO:L3_MISS" );
	if ((retval=PAPI_event_name_to_code(EventCodeStr, &native)) != PAPI_OK) {
	  printf("Event name to code failed: %d\n", retval);
	}
	if ((retval=PAPI_add_event(EventSet, native)) != PAPI_OK) {
	  printf("Event add failed: %d\n", retval);
	}
	
	sprintf( EventCodeStr, "OFFCORE_RESPONSE_1:ANY_RFO:LLC_MISS_LOCAL_DRAM" );
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_1:OTHER:L3_MISS" );
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_1:PF_DATA_RD:L3_MISS" );
	//sprintf( EventCodeStr, "OFFCORE_RESPONSE_1:PF_RFO:L3_MISS" );
	if ((retval=PAPI_event_name_to_code(EventCodeStr, &native)) != PAPI_OK) {
	  printf("Event name to code failed: %d\n", retval);
	}
	if ((retval=PAPI_add_event(EventSet, native)) != PAPI_OK) {
	  printf("Event add failed: %d\n", retval);
	}
#endif

	//Call the main computation
	gettimeofday(&time, NULL);
	elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000);
	
	
#ifdef PAPI
////PAPI///////////////////////////////////////////////
/* Start counting */
  if (PAPI_start(EventSet) != PAPI_OK)
      printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
////PAPI END///////////////////////////////////////////////
#endif	
	TMM(N, A, B, R);
#ifdef PAPI
////PAPI///////////////////////////////////////////////
  if (PAPI_read(EventSet, PAPIvalues) != PAPI_OK)
      printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
  if (PAPI_stop(EventSet, PAPIvalues) != PAPI_OK)
      printf ("%s:%d\t ERROR\n", __FILE__, __LINE__);
#endif        
	gettimeofday(&time, NULL);
	elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000) - elapsed_time;

	// timing information
	//printf("Execution time : %lf sec.\n", elapsed_time);
	
#ifdef PAPI
	printf("%ld\t%lf \t%lld \t%lld \t%lld \t%lld\n",N,elapsed_time,PAPIvalues[0],PAPIvalues[1],PAPIvalues[2],PAPIvalues[3]);
#else	
	printf("Execution time : %lf sec.\n", elapsed_time);
#endif	
	#ifdef TIMING
		FILE * fp = fopen( "trace.dat","a+");
		if (fp == NULL) {
				printf("I couldn't open trace.dat for writing.\n");
				exit(EXIT_FAILURE);
		}
		fprintf(fp, "%ld\t%lf\n",N,elapsed_time);
		fclose(fp);
	#endif
	
	//Verification Run
	#ifdef VERIFY
		#ifdef TIMING
			gettimeofday(&time, NULL);
			elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000);
		#endif
    	TMM_verify(N, A, B, R_verify);
    	#ifdef TIMING
    		gettimeofday(&time, NULL);
			elapsed_time = (((double) time.tv_sec) + ((double) time.tv_usec)/1000000) - elapsed_time;
			
			FILE * fp_verify = fopen( "trace_verify.dat","a+");
			if (fp == NULL) {
					printf("I couldn't open trace_verify.dat for writing.\n");
					exit(EXIT_FAILURE);
			}
			fprintf(fp, "%ld\t%lf\n",N,elapsed_time);
			fclose(fp_verify);
		#endif
	#endif
    	
	#ifdef CHECKING
    	//Print Outputs
    	
		
		{
			#ifdef NO_PROMPT
				#define S0(i,j) printf("%0.2f\n",var_R(i,j))
			#else
				#define S0(i,j) printf("R(%ld,%ld)=",(long) i,(long) j);printf("%0.2f\n",var_R(i,j))
			#endif
			int c1,c2;
			for(c1=1;c1 <= N;c1+=1)
			 {
			 	for(c2=c1;c2 <= N;c2+=1)
			 	 {
			 	 	S0((c1),(c2));
			 	 }
			 }
			#undef S0
		}
		
	#elif VERIFY
		//Compare outputs for verification
		{
			//Error Counter
			int _errors_ = 0;
			#define S0(i,j) if (fabsf(1.0f - var_R_verify(i,j)/var_R(i,j)) > EPSILON) _errors_++;
			int c1,c2;
			for(c1=1;c1 <= N;c1+=1)
			 {
			 	for(c2=c1;c2 <= N;c2+=1)
			 	 {
			 	 	S0((c1),(c2));
			 	 }
			 }
			#undef S0
			if(_errors_ == 0){
				printf("TEST for R PASSED\n");
			}else{
				printf("TEST for R FAILED. #Errors: %d\n", _errors_);
			}
		}
    #endif
    
	//Memory Free
	free(_lin_A);
	free(A);
	free(_lin_B);
	free(B);
	free(_lin_R);
	free(R);
	#ifdef VERIFY
		free(_lin_R_verify);
		free(R_verify);
	#endif
	
	return EXIT_SUCCESS;
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
#undef EPSILON
