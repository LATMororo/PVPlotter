import warnings
import pyvista   as pv
import pyvistaqt as pqt
import numpy     as np

from ..plotters.Plotter  import Plotter 
from ..mycolors.MyColors import myColors, myCMaps
from ..lsplot.IsoCurve   import getIsoCurve
from ..utils.Utils       import getFile 


#------------------------------------------------------------------------
#    class TLSPlot 
#------------------------------------------------------------------------

class TLSPlot(Plotter):

    def __init__(self, pl: pv.Plotter | pqt.BackgroundPlotter, 
                       lc: float, **kwargs):

        super().__init__(pl, **kwargs)

        assert isinstance(lc, float), "\'lc\' must be a float!"

        self.lc = lc
        self.actors = {} # actors w.r.t. iso curves and LS field

    #--------------------------------------------------------------------
    #    setMesh     
    #--------------------------------------------------------------------

    def setMesh(self, mesh: pv.UnstructuredGrid) -> None:

        super().setMesh(mesh) # set default mesh

        # Change some properties of the mesh.

        self.clim([0., self.lc*1.05])
        self.mactor.mapper.scalar_visibility = True
        self.mactor.mapper.lookup_table.cmap = myCMaps('tlsmap')

        self.pl.camera_position = self.cpos

    #--------------------------------------------------------------------
    #    addIsoZeroCurve
    #--------------------------------------------------------------------

    def addIsoZeroCurve(self, it: int) -> None:

        fname = getFile(it, 'iso0')

        if fname == '':
            return

        lines = getIsoCurve(fname)

        if lines == None or len(lines) == 0:
            return

        if 'iso0' not in self.actors.keys():
            self.actors['iso0'] = self.pl.add_lines(
                                    np.array(lines, dtype=np.float64), 
                                    color=myColors('dred'), 
                                    width=2.5,
                                    name='iso0')
        else:
            self.actors['iso0'].mapper.dataset.points=np.array(lines,dtype=np.float64)


    #--------------------------------------------------------------------
    #    addIsoLcCurve
    #--------------------------------------------------------------------

    def addIsoLcCurve(self, it: int) -> None:

        fname = getFile(it, 'isoLc')

        if fname == '':
            return

        lines  = getIsoCurve(fname)

        if lines == None or len(lines) == 0:
            return

        if 'isoLc' not in self.actors.keys():
            self.actors['isoLc'] = self.pl.add_lines(
                                    np.array(lines, dtype=np.float64), 
                                    color=myColors('dred'), 
                                    width=2.5,
                                    name='isoLc')
        else:
            self.actors['isoLc'].mapper.dataset.points=np.array(lines,dtype=np.float64)

    #--------------------------------------------------------------------
    #    addLSFieldData
    #--------------------------------------------------------------------

    def addLSFieldData(self, it: int) -> None:

        assert self.pl.mesh != None, "None mesh!"

        fname = getFile(it, 'ls')

        if fname == '':
            return

        # Get LS field data. 

        lsInfo = np.genfromtxt(
                fname, delimiter=',', dtype=[np.int32, np.float64])

        vals   = [ float('nan') for i in range(self.pl.mesh.n_points) ]

        for i in lsInfo:
            vals[i[0]] = i[1]

        self.pl.mesh.point_data['LSField'] = vals

    #--------------------------------------------------------------------
    #    plot 
    #--------------------------------------------------------------------

    def plot(self, it: int, **kwargs) -> None:
        
        assert self.pl != None, 'inactive plotter!'

        self.addLSFieldData (it)
        self.addIsoZeroCurve(it)
        self.addIsoLcCurve  (it)

    #--------------------------------------------------------------------
    #    runPlot 
    #--------------------------------------------------------------------
    
    def runPlot(self, it: int) -> None:

        self.pl.show(cpos='xy', interactive_update=True)

        while True:

            self.addLSFieldData (it)
            self.addIsoLcCurve  (it)
            self.addIsoZeroCurve(it)

            self.pl.update()

            key = input('quit? ')

            if key == 'q' or key == 'y' or key == 'yes':
                break

    #--------------------------------------------------------------------
    #    clear
    #--------------------------------------------------------------------

    def clear(self) -> None:

        for iact in self.actors.items():
            self.pl.remove_actor(iact)

        self.actors.clear()

        self.pl.mesh.point_data.pop('LSField', None)
