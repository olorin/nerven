nerven
======

nerven is a visualisation and capture utility for the Emotiv EPOC.
Currently it only runs (out of the box) on Linux; let me know if you 
get it working on another system.

Authors/contributors
====================

 * Sharif Olorin
 * Sarah Bennett (https://github.com/sarahbennett)

Requirements
============

* An unencrypted stream of EEG data (this can be obtained using emokitd
  from http://github.com/openyou/emokit)
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

