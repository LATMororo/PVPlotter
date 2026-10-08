from pyvista import CellType


#------------------------------------------------------------------------
#    class ElemType 
#------------------------------------------------------------------------


class ElemType:
    """
    This class helps to convert a Gmsh-type element to a Vkt-type element.
    """

    # TODO: it could be interesting to have the actual names of Gmsh.

    # Types based on Gmsh types.

    TYPES = {
            1:  ['Line2', 2],        # 2-node line
            2:  ['Triangle3', 3],    # 3-node triangle 
            3:  ['Quad4', 4],        # 4-node quadrangle
            4:  ['Tetrahedron4', 4], # 4-node tetrahedron
            5:  ['Brick8', 8],       # 8-node hexahedron
            9:  ['Triangle6', 6],    # 6-node second order triangle
            11: ['Tetrahedron10', 10], # 10-node tetrahedron
            15: ['Point', 1],        # 1-node point
            16: ['Quad8', 8],        # 8-node second order quadrangle
            }

    # Vtk related types.

    VTK_TYPES = {
            1:  CellType.LINE,
            2:  CellType.TRIANGLE,
            3:  CellType.QUAD,
            4:  CellType.TETRA,
            5:  CellType.HEXAHEDRON,
            9:  CellType.QUADRATIC_TRIANGLE,
            11: CellType.QUADRATIC_TETRA,
            15: CellType.VERTEX,
            16: CellType.QUADRATIC_QUAD,
            }

    #--------------------------------------------------------------------
    #    constructor, __init__
    #--------------------------------------------------------------------

    def __init__(self):
        pass

    #--------------------------------------------------------------------
    #    node_count
    #--------------------------------------------------------------------

    @staticmethod
    def node_count(etype):

        r = ElemType._check_type(etype, ElemType.node_count.__name__)

        return r[1]

    #--------------------------------------------------------------------
    #    to_vtk 
    #--------------------------------------------------------------------

    @staticmethod
    def to_vtk(etype):

        ElemType._check_type(etype, ElemType.to_vtk.__name__)

        return ElemType.VTK_TYPES[etype]


    #--------------------------------------------------------------------
    #    gmsh_to_jive_nodes_conn 
    #--------------------------------------------------------------------

    @staticmethod
    def gmsh_to_jive_nodes_conn(etype, inodes):

        ElemType._check_type(
                etype, ElemType.gmsh_to_jive_nodes_conn.__name__)

        if   etype == 9:
            pass
        elif etype == 16:
            pass

    #--------------------------------------------------------------------
    #    _check_type
    #--------------------------------------------------------------------

    @staticmethod
    def _check_type(etype, name_func):

        r = ElemType.TYPES.get(etype, None)

        if r is None:
            msg = 'ElemType.' + name_func + '(): Invalid element type \''\
                    + str(etype) + '\'!. The available types are '\
                    '(type, name): '

            for i, k in enumerate(ElemType.TYPES.keys()):

                name = ElemType.TYPES[k][0]

                if i == len(ElemType.TYPES.keys())-1:
                    msg += '\'' + str((k, name)) + '\'.'
                    break
                
                msg += ', ' + str((k, name))

            raise KeyError(msg)

        return r
