import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("nerven.epoc._parse", ["src/nerven/epoc/_parse.pyx"])
]

setup(name='nerven',
      version='0.1',
      author='Sharif Olorin',
      author_email='sio@tesser.org',
      requires=[
          'wxmpl',
          'scipy',
          'numpy',
          ],
      cmdclass={'build_ext' : build_ext},
      ext_modules=ext_modules,
      package_dir={'' : 'src'},
      packages=['nerven', 'nerven.epoc', 'nerven.writer'],
      package_data={'nerven' : ['img/*.png']},
      scripts=['src/nerven_gui'],
      data_files=[('bin', ['src/nerven_gui'])],
      )
