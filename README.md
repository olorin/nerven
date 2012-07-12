nerven
======

nerven is a visualisation and capture utility for the Emotiv EPOC. It
was written by Sharif Olorin, who can be reached at sio@tesser.org. 

requirements
============

* An unencrypted stream of EEG data (this can be obtained using the
  included daemon nervend, or with Kyle Machulis' emokit at 
  https://github.com/qdot/emokit)
* python-edf (my fork at https://bitbucket.org/fractalcat/python-edf)
* wxmpl (http://agni.phys.iit.edu/~kmcivor/wxmpl/)
* Cython (http://www.cython.org/)

installation
============

sudo python setup.py install