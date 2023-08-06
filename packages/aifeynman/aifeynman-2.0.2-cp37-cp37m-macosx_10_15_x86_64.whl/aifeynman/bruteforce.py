import glob
import os
from ctypes import CDLL, py_object

from . import __file__ as basedir

libfile = glob.glob(os.path.join(
    os.path.dirname(basedir), '_bruteforce*.so'))[0]

bruteforce = CDLL(libfile)

# Gradient Version
bruteforce.code1.restype = py_object
bruteforce.code1.argtypes = [py_object, py_object, py_object,
                             py_object, py_object, py_object, py_object, py_object]

# Normal Version
bruteforce.code2.restype = py_object
bruteforce.code2.argtypes = [py_object, py_object, py_object,
                             py_object, py_object, py_object, py_object, py_object]

# Additive and Multiplicatuve Constant solver
bruteforce.code3.restype = py_object
bruteforce.code3.argtypes = [py_object, py_object, py_object,
                             py_object, py_object, py_object, py_object, py_object]

# Additive and Multiplicatuve Constant solver
bruteforce.code4.restype = py_object
bruteforce.code4.argtypes = [py_object, py_object, py_object, py_object, py_object,
                             py_object, py_object, py_object, py_object, py_object]

# Additive and Multiplicatuve Constant solver
bruteforce.code5.restype = py_object
bruteforce.code5.argtypes = [py_object, py_object, py_object, py_object, py_object,
                             py_object, py_object, py_object, py_object, py_object]
