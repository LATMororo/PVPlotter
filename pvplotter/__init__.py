# -----------------------------------------------------------------------
# Import some stuff.
# -----------------------------------------------------------------------

'''
import sys

# -----------------------------------------------------------------------
# Set/append this package in the path. In this way, it is possible
# to use such package 'everywhere'.
# -----------------------------------------------------------------------

curr_dir = __file__

print(curr_dir)

curr_dir = curr_dir[:-11]

print(curr_dir)

sys.path.append(curr_dir)
'''

from .mesh     import * 
from .lsplot   import *
from .mycolors import *
from .plotters import *
from .tlsplot  import *
from .graph    import *

#__all__ = ['Gmsh']
