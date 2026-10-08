import pyvista as pv
import numpy   as np


from .Gmsh     import readGmsh
from .ElemType import ElemType


#------------------------------------------------------------------------
#    PyVistMesh 
#------------------------------------------------------------------------


def pyVistaMesh(nodes: list, elems: list) -> pv.UnstructuredGrid:

    # Build VTK/PyVist cells and cell_types arrays.

    cells = []
    cell_types = []

    # Loop over all cells.
    # NOTE: input argument 'elems' is actually a cell-type data struct.

    for icell in elems: 

        cells.append(ElemType.node_count(icell[0]))

        for inode in icell[1:]:
            cells.append(inode)

        cell_types.append(ElemType.to_vtk(icell[0]))

    # Get coordinates of nodes and add the 'z' coordinate if 2D 
    # simulation is being carried-out.

    rank = len(nodes[0])

    assert rank >= 1 and rank <= 3, "invalid rank"

    if rank == 2:
        coords = np.pad(nodes, ((0,0), (0,1))) 
    else:
        coords = np.vstack(nodes)

    return pv.UnstructuredGrid(cells, cell_types, coords)


#------------------------------------------------------------------------
#    readFromGmsh
#------------------------------------------------------------------------


def readFromGmsh(fname: str) -> pv.UnstructuredGrid:

    nodes, cells = readGmsh(fname)

    return pyVistaMesh(nodes, cells)
