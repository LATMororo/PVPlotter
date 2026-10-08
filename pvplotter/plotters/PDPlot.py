import pyvista      as pv
import pyvistaqt    as pqt
import numpy        as np
import numpy.typing as npt

from .JivePlot           import JivePlot
from ..mycolors.MyColors import myColors


#------------------------------------------------------------------------
#    class PDPlot
#------------------------------------------------------------------------

class PDPlot(JivePlot):

    def __init__(self, pl: pv.Plotter | pqt.BackgroundPlotter, **kwargs):

        super().__init__(pl, **kwargs)

        self.dataset = [] 
        self.actors  = {}

    #--------------------------------------------------------------------
    #    setMesh     
    #--------------------------------------------------------------------

    def setMesh(self, mesh: pv.UnstructuredGrid) -> None:

        super().setMesh(mesh)

        self.mactor.prop.show_edges = False
        self.mactor.prop.style = 'points'
        self.mactor.prop.point_size = 15
        self.mactor.prop.render_points_as_spheres = True

    #--------------------------------------------------------------------
    #    addPlot 
    #--------------------------------------------------------------------

    def addPlot(self, fname: str, **kwargs) -> None:

        super().plot(fname, **kwargs)

    #--------------------------------------------------------------------
    #    runPlot 
    #--------------------------------------------------------------------

    def runPlot(self, it: int) -> None:
        pass

    #--------------------------------------------------------------------
    #    clear 
    #--------------------------------------------------------------------

    def clear(self) -> None:

        super().clear()

        if 'bpts' in self.actors:
            self.pl.remove_actor(self.actors['bpts'])
            self.actors.pop('bpts')

        if 'rpts' in self.actors:
            self.pl.remove_actor(self.actors['rpts'])
            self.actors.pop('rpts')

        if 'dpts' in self.actors:
            self.pl.remove_actor(self.actors['dpts'])
            self.actors.pop('dpts')

        if 'bbonds' in self.actors:
            self.pl.remove_actor(self.actors['bbonds'])
            self.actors.pop('bbonds')

    #--------------------------------------------------------------------
    #    labelPDNType 
    #--------------------------------------------------------------------

    def labelPDNType(self, **kwargs) -> None:
         
        # Get PD node type file.

        data = np.genfromtxt(
                'pdntype.out', delimiter=',', dtype=[np.int32,np.int32])

        bpts  = [] # 0
        rpts  = [] # 1
        dpts  = [] # 2

        for i in data:
            if   i[1] == 0:
                bpts.append(i[0])
            elif i[1] == 1:
                rpts.append(i[0])
            elif i[1] == 2:
                dpts.append(i[0])
            else:
                raise RuntimeError(
                     'Node ' + str(i[1]) + ' with invalid PD node type!')

        bcolor = kwargs.get('bcolor', myColors('dorange'))
        rcolor = kwargs.get('rcolor', myColors('dblue'))
        dcolor = kwargs.get('dcolor', myColors('dgreen'))

        bsize  = kwargs.get('bsize', 5)
        rsize  = kwargs.get('rsize', 5)
        dsize  = kwargs.get('dsize', 5)

        points = self.points0.copy() #self.pl.mesh.points.copy()

        self.actors['bpts'] = self.pl.add_points(points[bpts], 
                                                 render_points_as_spheres=True, 
                                                 color=bcolor,
                                                 point_size=bsize,
                                                 name='bpts')

        self.actors['rpts'] = self.pl.add_points(points[rpts], 
                                                 render_points_as_spheres=True, 
                                                 color=rcolor,
                                                 point_size=rsize,
                                                 name='rpts')

        self.actors['dpts'] = self.pl.add_points(points[dpts], 
                                                 render_points_as_spheres=True, 
                                                 color=dcolor,
                                                 point_size=dsize,
                                                 name='dpts')

    #--------------------------------------------------------------------
    #    addBrokenBonds
    #--------------------------------------------------------------------

    def addBrokenBonds(self, it: int, **kwargs) -> None:

        # Get node indices that form broken bonds.

        fname = 'bstatus.' + str(it) + '.out' 

        bnodes = np.genfromtxt(
                       fname, delimiter=',', dtype=[np.int32, np.int32])

        # Loop over bonds and add them in plotter object, 'pl'. 

        lines = []

        for bond in bnodes:
            lines.append(self.pl.mesh.points[bond[0]])
            lines.append(self.pl.mesh.points[bond[1]])

        c = kwargs.get('color', myColors('dblue'))
        w = kwargs.get('width', 2.5)

        self.actors['bbonds'] = self.pl.add_lines(np.array(lines, dtype=np.float64), 
                                                  color=c, width=w)
