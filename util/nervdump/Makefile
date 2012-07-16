CC = "gcc"
CCARGS = "-g"

all: nervdump

epoc.o :
	$(CC) $(CCARGS) -c epoc.c -o epoc.o

edflib.o : 
	$(CC) $(CCARGS) -c edflib.c -o edflib.o

nervdump.o :
	$(CC) $(CCARGS) -c nervdump.c -o nervdump.o

nervdump : epoc.o edflib.o nervdump.o
	$(CC) $(CCARGS) -o nervdump epoc.o edflib.o nervdump.o -lemokit -lusb-1.0 -lmcrypt -lpthread

clean:
	rm -f *.o nervdump
