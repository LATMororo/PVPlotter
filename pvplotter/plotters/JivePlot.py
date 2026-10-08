import warnings
import pyvista      as pv
import pyvistaqt    as pqt
import numpy        as np
import numpy.typing as npt

from xml.etree import ElementTree as ET

from ..plotters.Plotter  import Plotter 
from ..mycolors.MyColors import myColors, myCMaps
from ..utils.Utils       import getFile 


#------------------------------------------------------------------------
#    class JivePlot 
#------------------------------------------------------------------------

class JivePlot(Plotter):

    def __init__(self, pl: pv.Plotter | pqt.BackgroundPlotter, **kwargs):

        super().__init__(pl, **kwargs)

        self.dataset = [] 
        self.points0 = None

    #--------------------------------------------------------------------
    #    setMesh     
    #--------------------------------------------------------------------

    def setMesh(self, mesh: pv.UnstructuredGrid) -> None:

        super().setMesh(mesh)

        self.mactor.mapper.scalar_visibility = True
        self.pl.camera_position = self.cpos
        self.points0 = mesh.points.copy()

    #--------------------------------------------------------------------
    #    addPlot 
    #--------------------------------------------------------------------

    def addPlot(self, fname: str, **kwargs) -> None:
        
        """
        fname = getFile(it, 'mechout')

        if fname == '':
            return
        """

        tableType = kwargs.get('tableType', None)
        dataType  = kwargs.get('dataType', None)
        comp      = kwargs.get('comp', None)
        scale     = kwargs.get('scale', 0.)

        if tableType == None:
            raise RuntimeError("Empty \'tableType\'!")

        if dataType == None:
            raise RuntimeError("Empty \'dataType\'!")


        header, data = self.findTable(fname, tableType, dataType)

        if len(header) > 0 and len(data) > 0: 
            self.addPointField(header, data, dataType, comp)
            self.updateCoords(fname, scale)

    #--------------------------------------------------------------------
    #    runPlot 
    #--------------------------------------------------------------------

    def runPlot(self, fname: str) -> None:
        pass

    #--------------------------------------------------------------------
    #    clear 
    #--------------------------------------------------------------------

    def clear(self) -> None:

        for d in self.dataset:
            self.pl.mesh.point_data.pop(d, None)

        self.dataset.clear()

    #--------------------------------------------------------------------
    #    updateCoords 
    #--------------------------------------------------------------------

    def updateCoords(self, fname: str, scale: float) -> None:

        assert self.pl.mesh != None, "None mesh!"

        if scale <= 0.:
            return
        
        """
        fname = getFile(it, 'mechout')

        if fname == '':
            return
        """

        header, data = self.findTable(fname, 'NodeTable', 'disp')

        rank = len(header)

        for d in data: 
            nodeIdx = d[0] - 1 
            for ir in range(rank):
                self.pl.mesh.points[nodeIdx][ir] = self.points0[nodeIdx][ir] + d[ir+1] * scale

    #--------------------------------------------------------------------
    #    addField
    #--------------------------------------------------------------------

    def addPointField(self, 
                      header: dict, 
                      data: npt.NDArray, 
                      dataType: str, 
                      comp: str='mag') -> None: 

        assert self.pl.mesh != None, "None mesh!"

        # Check if 'comp' is a valid component.

        if comp == None:
            raise RuntimeError('\'None\' component!')

        okComp = False
        if comp == 'mag':
            okComp = True
        elif comp in header:
            okComp = True

        if not okComp:
            raise RuntimeError(f"Component `{comp}\' not found!")

        # All points have NaN value at the beginning.

        vals = [float('nan') for i in range(self.pl.mesh.n_points)]

        if comp == 'mag':

            for d in data:
                nodeID = d[0]-1 # JIVE does not output in C-style index
                ivals = [d[i] for i in range(1,len(d))]
                vals[nodeID] = np.linalg.norm(ivals)

        else:
            # Get the column of the component.

            colComp = header.index(comp)
        
            # Add 1 to column index. 

            colComp += 1 # add 1. 
        
            for d in data:
                vals[d[0]-1] = d[colComp]

        dsName = dataType + '-' + comp # dataset name
        self.dataset.append(dsName)
        self.pl.mesh.point_data[dsName] = vals

    #--------------------------------------------------------------------
    #    findTable
    #--------------------------------------------------------------------

    @staticmethod
    def findTable(fname: str, 
                  tableType: str, 
                  dataType: str) -> dict | npt.NDArray[np.dtype[np.float64]]:

        """ tableType = NodeTable or ElementTable
            dataType  = disp, stress, strain, . . .
        """

        # Get all the content of a given XML file. 

        content = ''

        with open(fname, 'r') as f:
            content = f.read()

            # Remove blank lines. 

            content = "".join([s for s in content.splitlines(True) if s.strip()])

        if content == '':
            return None, None

        # Wrap the content whithin a single root element.

        content = '<root>\n' +  content + '</root>'

        root = ET.fromstring(content)

        # Process the elements. 

        elements = root.iter(tableType)

        for elem in elements:

            name = elem.attrib.get('name', None)

            if name == dataType:
                table  = elem.find('Section')
                header = [d.strip() for d in table.attrib['columns'].split("|")]

                data = [l for l in table.text.splitlines() if len(l.strip()) > 0]

                numData = len([d.strip() for d in data[0].split()])

                dtypes = []

                for d in range(numData):
                    if d == 0:
                        dtypes.append(np.int32)
                    else:
                        dtypes.append(np.float64)

                data = np.genfromtxt(data, dtype=dtypes)

                return header, data

        return None, None


