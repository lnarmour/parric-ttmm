#include <stdio.h>
#include <stdlib.h>

int multiply(int, int);

int main(int argc, char** argv) {
	int x = atoi(argv[1]);
	int y = atoi(argv[2]);
	printf("%d * %d = %d\n (ttmm-0)", x, y, multiply(x,y));
	return 0;
}

int multiply(int x, int y) {
	return x*y;
}
