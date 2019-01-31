#include <boost/numeric/ublas/matrix.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <limits.h>
#include <float.h>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include <chrono>
#include "TMM_known_good.c"
void TMM(long, long, long, long, float**, float**, float**);
using namespace std;

int main(int argc, char** argv){
	if(argc!=2){
		cerr<<"Use: "<<argv[0]<<" <N>\n";
		return 1;
	}
	srand(time(0));
	//read N from first argument
	long N;
	stringstream ss;
	ss<<argv[1];
	ss>>N;
	//now make empty matrices in the format that alphaz expects
	float **a, **b, **c, **d;
	a=new float*[N+1];
	for(int i=0;i<N+1;i++)
		a[i]=new float[N+1];
	b=new float*[N+1];
	for(int i=0;i<N+1;i++)
		b[i]=new float[N+1];
	c=new float*[N+1];
	for(int i=0;i<N+1;i++){
		c[i]=new float[N+1];
	}
	d=new float*[N+1];
	for(int i=0;i<N+1;i++){
		d[i]=new float[N+1];
	}
	//generate A randomly
	for(int i=0;i<N;i++){	
		for(int j=0;j<N;j++){
			a[i+1][j+1]=j<i?0:rand()%15;
		}
	}
	//generate B randomly
	for(int i=0;i<N;i++){
		for(int j=0;j<N;j++){
			b[i+1][j+1]=j<i?0:rand()%15;
		}
	}
	//now call the alphaz routine
	auto start= chrono::system_clock::now();



	TMM(N,N,N,N,a,b,c);



	auto end= chrono::system_clock::now();
	chrono::duration<double> elapsed_seconds = end-start;
	TMM_good(N, a, b, d);
	
	for(int i=1;i<=N;i++)
		for(int j=i;j<=N;j++){
			if (abs(c[i][j]-d[i][j]) > .01)
				cerr<<"result at ("<<i<<", "<<j<<") was "<<d[i][j]<<" instead of "<<a[i][j]<<".\n";
		}
	for(int i =0; i <=N; i++)
		delete[] a[i];
	delete[] a;
	for(int i =0; i <=N; i++)
		delete[] b[i];
	delete[] b;
	for(int i =0; i <=N; i++)
		delete[] c[i];
	delete[] c;
	for(int i =0; i <=N; i++)
		delete[] d[i];
	delete[] d;
	cout<<"Alphaz time: "<<elapsed_seconds.count()<<"\n";
	return 0;
}
