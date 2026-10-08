import numpy      as np
import matplotlib as mtl


#------------------------------------------------------------------------
#    myColors
#------------------------------------------------------------------------

def myColors(name):

    match name:

        case 'dblue':
            return np.array([0., 0.2, 0.6, 1.], dtype=np.float32)

        case 'dgray':
            return np.array([0.3, 0.3, 0.3, 1.], dtype=np.float32)

        case 'dred':
            return np.array([0.7, 0., 0., 1.], dtype=np.float32)

        case 'dgreen':
            return np.array([0., 0.5, 0., 1.], dtype=np.float32)

        case 'dorange':
            return np.array(
                    [180./255., 40./255., 0., 1.], dtype=np.float32)

        case _:

            raise RuntimeError(
                    "Color \'" + str(name) + "\' not supported!")

#------------------------------------------------------------------------
#    myCMaps
#------------------------------------------------------------------------

def myCMaps(name):

    match name:

        case 'tlsmap':

            tlscolor = np.array([
                [0.5020,    0.5804,    0.6196, 1.],
                [0.5181,    0.5961,    0.6345, 1.],
                [0.5342,    0.6118,    0.6493, 1.],
                [0.5503,    0.6275,    0.6642, 1.],
                [0.5664,    0.6431,    0.6790, 1.],
                [0.5825,    0.6588,    0.6939, 1.],
                [0.5986,    0.6745,    0.7088, 1.],
                [0.6147,    0.6902,    0.7236, 1.],
                [0.6308,    0.7059,    0.7385, 1.],
                [0.6469,    0.7216,    0.7533, 1.],
                [0.6630,    0.7373,    0.7682, 1.],
                [0.6791,    0.7529,    0.7831, 1.],
                [0.6952,    0.7686,    0.7979, 1.],
                [0.7113,    0.7843,    0.8128, 1.],
                [0.7274,    0.8000,    0.8277, 1.],
                [0.7435,    0.8157,    0.8425, 1.],
                [0.7596,    0.8314,    0.8574, 1.],
                [0.7756,    0.8471,    0.8722, 1.],
                [0.7917,    0.8627,    0.8871, 1.],
                [0.8078,    0.8784,    0.9020, 1.],
                [0.9922,    0.9686,    0.8431, 1.]], dtype=np.float32)

            return mtl.colors.ListedColormap(tlscolor, name='tlscmap')

        case _:
            raise RuntimeError(
                    "Color map \'" + str(name) + "\' not supported")

