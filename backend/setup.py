from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("cyton/core/model.pyx"),
    include_dirs=[numpy.get_include()],
)
