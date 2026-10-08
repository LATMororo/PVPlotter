import warnings
import pyvista   as pv
import pyvistaqt as pqt

from abc       import ABC, abstractmethod
from pyvistaqt import BackgroundPlotter

from ..utils.Utils  import getFile 


#------------------------------------------------------------------------
#    class Plotter
#------------------------------------------------------------------------

class Plotter(ABC):

    def __init__(self, pl: pv.Plotter | pqt.BackgroundPlotter, **kwargs):

        self.pl = pl 

        self.cpos    = kwargs.get('cpos', 'xy')
        self.mactor  = None
        self.lactors = {}

    #--------------------------------------------------------------------
    #    setMesh     
    #--------------------------------------------------------------------

    @abstractmethod
    def setMesh(self, mesh: pv.UnstructuredGrid) -> None:

        # Set only one mesh.

        assert self.mactor == None, "set only one mesh!"

        name = 'mesh0'

        self.mactor = self.pl.add_mesh(mesh, show_edges=True, name=name) 
    
    #--------------------------------------------------------------------
    #    addPlot 
    #--------------------------------------------------------------------

    @abstractmethod
    def addPlot(self, fname: str, **kwargs) -> None:
        pass

    #--------------------------------------------------------------------
    #    runPlot 
    #--------------------------------------------------------------------

    @abstractmethod
    def runPlot(self, fname: str) -> None:
        pass

    #--------------------------------------------------------------------
    #    clear
    #--------------------------------------------------------------------

    @abstractmethod
    def clear(self) -> None:
        pass

    #--------------------------------------------------------------------
    #    labelPoints
    #--------------------------------------------------------------------

    def labelPoints(self, inodes: list=None) -> None:

        assert self.pl.mesh != None, "None mesh!"

        if inodes == None:
            labels = [str(i) for i in range(self.pl.mesh.n_points)] 
            inodes = [i for i in range(self.pl.mesh.n_points)]

        elif isinstance(inodes, list):
            labels = [str(i) for i in inodes]

        elif isinstance(inodes, int):
            labels = [str(inodes)]
            inodes = [inodes]

        points = self.pl.mesh.points[inodes]

        #NOTE: show_points is set to 'False' in order to avoid deleting
        #      the original mesh. PyVista makes use of the original mesh 
        #      for rendering nodes. Once the user delete point labels, 
        #      PyVista also deletes nodes of the original mesh.

        self.lactors['lpoints'] = self.pl.add_point_labels(
                points,labels, 
                show_points=False, 
                text_color='black',
                name='lpoints')

    #--------------------------------------------------------------------
    #    labelElems
    #--------------------------------------------------------------------

    def labelElems(self, ielems: list=None) -> None:

        assert self.pl.mesh != None, "None mesh!"

        if ielems == None:
            labels = [str(i) for i in range(self.pl.mesh.n_cells)] 
            ielems = [i for i in range(self.pl.mesh.n_cells)]

        elif isinstance(ielems, list):
            labels = [str(i) for i in ielems]

        elif isinstance(ielems, int):
            labels = [str(ielems)]
            ielems = [ielems]

        points = self.pl.mesh.cell_centers().points[ielems]

        #NOTE: show_points is set to 'False' in order to avoid deleting
        #      the original mesh. PyVista makes use of the original mesh 
        #      for rendering nodes. Once the user delete point labels, 
        #      PyVista also deletes nodes of the original mesh.

        self.lactors['lelems'] = self.pl.add_point_labels(
                points,labels, 
                show_points=False, 
                text_color = 'yellow',
                name='lelems')

    #--------------------------------------------------------------------
    #    removeLabels
    #--------------------------------------------------------------------

    def removeLabels(self) -> None:

        if 'lpoints' in self.lactors.keys():
            self.pl.remove_actor(self.lactors['lpoints'])

        if 'lelems' in self.lactors.keys():
            self.pl.remove_actor(self.lactors['lelems'])

    #--------------------------------------------------------------------
    #    clim
    #--------------------------------------------------------------------

    def clim(self, clim: list) -> None:

        assert self.mactor.mapper != None, "None mesh mapper!"

        self.mactor.mapper.scalar_range = clim
