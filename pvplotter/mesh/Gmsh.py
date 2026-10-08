import gmsh
import numpy as np

from .ElemType import ElemType 


#------------------------------------------------------------------------
#    readGmsh
#------------------------------------------------------------------------


def readGmsh(fname: str ) -> list | list:
    """This function reads a mesh developed by using Gmsh. It returns 
    nodes and cells in a format used by PyVista.

    Args:
        fname (str): file name

    Returns:
        list (float): list of coordinates for each node on the mesh
        list (int): cells that form element, i.e., node connectivity

    Raises:
        RuntimeError 
    """

    gmsh.initialize()

    print('-------------------------------------------------------------')
    print('Gmsh Info ...')
    print('-------------------------------------------------------------')
    # gmsh.option.setNumber("General.Terminal", 1)

    gmsh.open(fname)

    # Read nodes.

    dim = gmsh.model.getDimension()

    nodeTags, nodeCoords,_ = gmsh.model.mesh.getNodes()

    nodes = np.zeros((len(nodeTags), dim), dtype=np.float64) 

    for i, ntag in enumerate(nodeTags):
        ntag = int(ntag-1)
        coords = [j for j in nodeCoords[3*i:(3+3*i)]]

        nodes[ntag] = coords[0:dim]

    # Read elements.

    elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements()

    if len(elemTypes) > 1:
        raise RuntimeError('Gmsh: Only one element type is allowed '\
                      'in the whole mesh!')

    nnodes = -1 # number of nodes per element

    elem_type = elemTypes[0]

    #NOTE: ElemType could check this...

    match elem_type:

        case 2:
            nnodes = 3  #T3
        case 3:
            nnodes = 4  #Q4
        case 4:
            nnodes = 4  #4-node tetrahedron
        case 5:
            nnodes = 8  #Brick8
        case 11:
            nnodes = 10 #TET10
        case _:
            raise RuntimeError('Gmsh: Unsupported element type!')

    assert nnodes*len(elemTags[0]) == len(elemNodeTags[0])

    # Build cells: [elem_type, node indices] 

    cells = []

    perm = np.zeros( nnodes, dtype=np.int8 )

    if nnodes == 10 and elem_type == 11:
        perm[0] = 0
        perm[1] = 1
        perm[2] = 2
        perm[3] = 3
        perm[4] = 4
        perm[5] = 5
        perm[6] = 6
        perm[7] = 7
        perm[8] = 9
        perm[9] = 8
    else:
        for i in range(nnodes):
            perm[i] = i

    for i in range(len(elemTags[0])):

        icells = []
        icells.append(int(elem_type))

        inodes = elemNodeTags[0][nnodes*i:(nnodes+nnodes*i)]
        inodes -= 1

        for j in perm:
            icells.append(int(inodes[j]))

#        for j in inodes:
#            icells.append(int(j))

        cells.append(icells)

    gmsh.clear()

    gmsh.finalize()

    return nodes, cells
