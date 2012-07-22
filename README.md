nerven
======

nerven is a visualisation and capture utility for the Emotiv EPOC. It
was written by Sharif Olorin (sio@tesser.org) with contributions from 
Sarah Bennett (https://github.com/sarahbennett).

Currently it only runs (out of the box) on Linux; if you use another
operating system and would like to use nerven, email me.

Requirements
============

* An unencrypted stream of EEG data (this can be obtained using nervend 
  at https://github.com/fractalcat/nervend)
* wxmpl (http://agni.phys.iit.edu/~kmcivor/wxmpl/)
* Cython (http://www.cython.org/) (required for performance improvements, but 
  nerven will run without it)

In addition, python-edf (https://bitbucket.org/cleemesser/python-edf/)
is required to capture to EDF files.

Installation
============

Linux
=====

sudo python setup.py install

