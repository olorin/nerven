#! /usr/bin/python

'''Creates a dummy FIFO from a sample EPOC data file - written for
dependency injection during development. The included epoc-dump-0.epoc
is a 20-second dump of my brain activity with generally good contact
quality.''' 

import sys, time

def main():
    args = sys.argv
    if len(args) < 3:
        print("usage: %s <dummy data file> <output path>" % args[0])
        return 1
    data = []
    with open(args[1], 'rb') as f:
        pkt = f.read(32)
        while pkt:
            data.append(pkt)
            pkt = f.read(32)
    print("Read %d packets." % len(data))
    with open(args[2], 'wb') as f:
        while True:
            for pkt in data:
                f.write(pkt)
                time.sleep(1.0/128.0)
        

if __name__ == '__main__':
    sys.exit(main())
