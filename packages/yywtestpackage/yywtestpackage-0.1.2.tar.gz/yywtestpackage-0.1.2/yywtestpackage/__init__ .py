from . import myfunction

from .myfunction import *

__all__ = ['myfunction']

__all__.extend(myfunction.__all__)

submodules = (myfunction)

__version__ = '0.1.2'