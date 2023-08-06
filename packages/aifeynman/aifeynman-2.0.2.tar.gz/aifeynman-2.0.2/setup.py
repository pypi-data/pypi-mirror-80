from ctypes import *

import setuptools
from numpy.distutils.core import Extension, setup

sr1 = Extension(name='aifeynman._symbolic_regress1', sources=[
    'aifeynman/symbolic_regress1.f90'])

sr2 = Extension(name='aifeynman._symbolic_regress2', sources=[
    'aifeynman/symbolic_regress2.f90'])

sr3 = Extension(name='aifeynman._symbolic_regress3', sources=[
    'aifeynman/symbolic_regress3.f90'])

sr_mdl4 = Extension(name='aifeynman._symbolic_regress_mdl4', sources=[
    'aifeynman/symbolic_regress_mdl4.f90'])

sr_mdl5 = Extension(name='aifeynman._symbolic_regress_mdl5', sources=[
    'aifeynman/symbolic_regress_mdl5.f90'])

newsr = Extension(name='aifeynman._bruteforce',
                  sources=['aifeynman/bruteforce.cpp'],
                  libraries=['gsl', 'gslcblas'],
                  extra_compile_args=['-std=c++11'])

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aifeynman',
    version='2.0.2',
    description='AI Feynman: a Physics-Inspired Method for Symbolic Regression',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SJ001/aifeynman',
    author='Silviu-Marian Udrescu',
    author_email='sudrescu@mit.edu',
    license='MIT',
    packages=['aifeynman'],
    package_dir={'aifeynman': 'aifeynman'},
    package_data={'aifeynman': ['*.txt', '*.f90']},
    include_package_data=True,
    ext_modules=[sr1, sr2, sr3, sr_mdl4, sr_mdl5, newsr],
    python_requires='>3.6',
    install_requires=['matplotlib',
                      'numpy',
                      'seaborn',
                      'sklearn',
                      'sortedcontainers',
                      'sympy >= 1.4',
                      'torch >= 1.4.0',
                      'torchvision',
                      ],
    entry_points={
        'console_scripts': [
            'feynman_sr1 = aifeynman._symbolic_regress1:go',
            'feynman_sr2 = aifeynman._symbolic_regress2:go',
            'feynman_sr3 = aifeynman._symbolic_regress3:go',
            'feynman_sr_mdl4 = aifeynman._symbolic_regress_mdl4:go',
            'feynman_sr_mdl5 = aifeynman._symbolic_regress_mdl5:go',
        ]}
)
