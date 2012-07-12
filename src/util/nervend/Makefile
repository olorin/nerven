CC = gcc
BUILDDIR = build
SRCDIR = src

all: nervend

nervend.o :
	gcc -c $(SRCDIR)/nervend.c -o $(BUILDDIR)/nervend.o

nervend : nervend.o
	gcc -o nervend $(BUILDDIR)/nervend.o -lemokit -lusb-1.0 -lmcrypt -lpthread

clean:
	rm -f build/*.o rm nervend
