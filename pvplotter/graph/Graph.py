import os
import warnings
import matplotlib.pyplot as plt
import numpy             as np

from   numpy.typing import NDArray

from ..utils.Utils  import searchForFilesExt


#------------------------------------------------------------------------
#    lodi
#------------------------------------------------------------------------


def lodi(show_plot: bool=True, fname: str=None) -> NDArray[np.float64]:

    # Search for 'lodi.out' file.

    if fname is None: # try to get it from the current folder

        fname = ''

        currDir = os.getcwd()

        for f in os.listdir(currDir):
            if f == 'lodi.out':
                fname = 'lodi.out'
                break

        if fname == '':
            raise RuntimeError('\'lodi.dat\' file not found!')

    # Get data.

    curve = np.genfromtxt(fname, delimiter=',', dtype=np.float64)

    # Check if the file has some data; otherwise, return.

    if len(curve) == 0:
        warnings.warn('no data available!')
        return

    if show_plot:
        fig, ax = plt.subplots()
        ax.plot(curve[:,1], curve[:,2])

        ax.set_xlabel('Displacement')
        ax.set_ylabel('Load')
        # ax.grid(True)

        plt.show()

    return curve


