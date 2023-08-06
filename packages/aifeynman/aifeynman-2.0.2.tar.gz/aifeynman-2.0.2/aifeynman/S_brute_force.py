# runs BF on data and saves the best RPN expressions in results.dat
# all the .dat files are created after I run this script
# the .scr are needed to run the fortran code

import csv
import ctypes
import os
import shutil
import subprocess
import sys
from subprocess import call

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

from .bruteforce import bruteforce
from .resources import _get_resource

# sep_type = 3 for add and 2 for mult and 1 for normal


def brute_force(pathdir, filename, BF_try_time, BF_ops_file_type, sep_type="*", sigma=10, band=0):
    try_time = BF_try_time
    try_time_prefactor = BF_try_time
    file_type = _get_resource(BF_ops_file_type)
    arityfile = _get_resource("arity2templates.txt")

    try:
        os.remove("results.dat")
    except:
        pass

    try:
        os.remove("brute_solutions.dat")
    except:
        pass

    try:
        os.remove("brute_constant.dat")
    except:
        pass

    try:
        os.remove("brute_formulas.dat")
    except:
        pass

    print("Trying to solve mysteries with brute force...")
    print("Trying to solve {}".format(pathdir+filename))

    shutil.copy2(pathdir+filename, "mystery.dat")

    if sep_type == "*":
        try:
            result = bruteforce.code4(list(pathdir.encode()), len(pathdir),
                                      list(filename.encode()), len(filename),
                                      list(file_type.encode()), len(file_type),
                                      list(arityfile.encode()), len(arityfile),
                                      10.0,
                                      BF_try_time)
        except:
            print("EXCEPTION IN S_bruteforce.py. sep_type '*'")
    if sep_type == "+":
        try:
            result = bruteforce.code5(list(pathdir.encode()), len(pathdir),
                                      list(filename.encode()), len(filename),
                                      list(file_type.encode()), len(file_type),
                                      list(arityfile.encode()), len(arityfile),
                                      10.0,
                                      BF_try_time)
        except:
            print("EXCEPTION IN S_bruteforce.py. sep_type '+'")

    result = np.array(result).T
    np.savetxt("results.dat", result, fmt="%s %s")
