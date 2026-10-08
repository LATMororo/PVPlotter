import numpy   as np


#------------------------------------------------------------------------
#    getIsoCurve
#------------------------------------------------------------------------


def getIsoCurve(fname: str) -> list:

    # Get segment points.

    points = np.loadtxt(fname, delimiter=',', dtype=np.float64)

    # Check if the file has some data; otherwise, return.

    if len(points) == 0:
        return

    # Add the 'z' coordinate if a 2D simulation is being carried-out.

    rank = len(points[0]) // 2 # two points per segment

    assert rank == 2 or rank == 3

    lines = []

    for point in points:

        if rank == 2:
            lines.append( np.pad(point[0:rank], (0,1)) ) # first point 
            lines.append( np.pad(point[rank: ], (0,1)) ) # second point 
        else:
            lines.append( point[0:rank] )
            lines.append( point[rank: ] )

    return lines
