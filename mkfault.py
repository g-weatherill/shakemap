#!/usr/bin/env python

#stdlib imports
from copy import deepcopy
import argparse
import os.path
from datetime import datetime

#third party imports
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from shakemap.grind.fault import Fault
from openquake.hazardlib.geo import point
from openquake.hazardlib.geo.utils import get_orthographic_projection
import sys
        
def main(pargs):
    nargin = len(pargs.coords)
    if nargin < 6:
        print 'You must specify at least two top edge points each with (x y z) coordinates.'
        sys.exit(1)
    if (nargin % 3) != 0:
        print 'Each point must have 3 coordinates (x y z) per top edge point.'
        sys.exit(1)
    npoints = nargin/3
    nquads = ((npoints*2 - 4)/2) + 1
    if pargs.widths is None or len(pargs.widths) != nquads:
        print 'You must specify %i widths' % nquads
        sys.exit(1)
    if pargs.dips is not None and pargs.depths is not None:
        print 'You must specify %i depths or %i dips, not both.' % (nquads,nquads)
        sys.exit(1)
    
    x = np.array(pargs.coords[1::3])
    y = np.array(pargs.coords[0::3])
    z = np.array(pargs.coords[2::3])
    
    fault = Fault.fromTrace(x,y,z,pargs.widths,pargs.dips)

    if pargs.plotfile:
        fig = plt.figure()
        ax0 = fig.add_subplot(2,1,1)
        ax1 = fig.add_subplot(2,1,2, projection='3d')
        for quad in fault.getQuadrilaterals():
            P0,P1,P2,P3 = quad
            xp = np.array([P0.longitude,P1.longitude,P2.longitude,P3.longitude,P0.longitude])
            yp = np.array([P0.latitude,P1.latitude,P2.latitude,P3.latitude,P0.latitude])
            zp = np.array([-P0.depth,-P1.depth,-P2.depth,-P3.depth,-P0.depth])
            ax0.plot(xp,yp)
            ax0.set_xlabel('Longitude')
            ax0.set_xlabel('Latitude')
            ax1.plot(xp,yp,zp)
            ax1.set_xlabel('Longitude')
            ax1.set_xlabel('Latitude')
            ax1.set_zlabel('Depth')
            ax0.axis('equal')
            ax1.axis('equal')
        plt.savefig(pargs.plotfile)

    if pargs.outfile:
        fault.writeFaultFile(pargs.outfile)
    
    
if __name__ == '__main__':
    desc = '''Create a multi-segment fault file.  Each segment can only contain one quadrilateral.
    Usage:
    Create a two segment fault where the top edge depths are 0 and the bottom edge depths are 25 and 35 km, with widths of 10 and 12 km. 
    %(prog)s 34.261757 -118.300781 0 34.442982 -118.359146 0 34.642071 -118.346786 0 -w 10.0 12.0 -d 25.0 35.0
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('coords', type=float, nargs='+',
                        help='Top edge coordinates')
    parser.add_argument('-w','--widths', dest='widths', type=float,nargs='+', help='specify widths (must match number of quads)')
    parser.add_argument('-d','--dips', dest='dips', type=float,nargs='+', help='specify dips (must match number of quads)')
    parser.add_argument('-p','--plotfile', dest='plotfile',type=str,help='Generate a plot of the fault')
    parser.add_argument('-o','--outfile', dest='outfile', type=str, help='specify output fault text file')
    args = parser.parse_args()
    main(args)

    

    
