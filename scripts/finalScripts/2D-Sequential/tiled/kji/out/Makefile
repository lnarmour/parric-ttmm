CFLAGS=  -O3  -std=c99  -I/usr/include/malloc/ 
LIBRARIES=-lm
CC=gcc
LD=xild
AR=xiar
OBJS = TMM.o 
all: plain check

debug: CFLAGS =-DDEBUG -g -Wall -Wextra -std=c99 -I/usr/include/malloc/
debug: all
		
plain: $(OBJS)
	$(CC) TMM-wrapper.c -o TMM $(OBJS) $(CFLAGS) $(LIBRARIES)

check: $(OBJS)
	$(CC) TMM-wrapper.c -o TMM.check $(OBJS) $(CFLAGS) $(LIBRARIES) -DCHECKING

verify: $(OBJS) TMM_verify.o
	$(CC) TMM-wrapper.c -o TMM.verify $(OBJS) TMM_verify.o $(CFLAGS) $(LIBRARIES) -DVERIFY

verify-rand: $(OBJS) TMM_verify.o
	$(CC) TMM-wrapper.c -o TMM.verify-rand $(OBJS) TMM_verify.o $(CFLAGS) $(LIBRARIES) -DVERIFY -DRANDOM

TMM.o : TMM.c
	$(CC) TMM.c -o TMM.o $(CFLAGS) $(LIBRARIES) -c

TMM_verify.o : TMM_verify.c
	$(CC) TMM_verify.c -o TMM_verify.o $(CFLAGS) $(LIBRARIES) -c

clean:
	rm -f *.o TMM TMM.check TMM.verify TMM.verify-rand
