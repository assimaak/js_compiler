CC = gcc
CFLAGS = -Wall -Wextra -g

all: 12-fact glob-loc-arg 01-expressions compiled

compiled: base.o compiled.o
	$(CC) $(CFLAGS) -o $@ $^

01-expressions: base.o 01-expressions.o
	$(CC) $(CFLAGS) -o $@ $^

12-fact: base.o 12-fact.o
	$(CC) $(CFLAGS) -o $@ $^

glob-loc-arg: base.o glob-loc-arg.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f core *.o *.s

realclean: clean
	rm -f ${all}

base.o: hacks.h base.h
12-fact.o: hacks.h base.h
01-expressions.o: hacks.h base.h
glob-loc-arg.o: hacks.h base.h
compiled.o: hacks.h base.h

.PHONY: all
