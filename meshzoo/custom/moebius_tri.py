#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh on a Möbius strip.
'''
import numpy as np
from math import pi, sin, cos


def create_moebius_mesh(num, index):
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = num[0]
    # Number of nodes along the width of the strip (>= 2)
    nw = num[1]

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # l = 5
    p = 1.5

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\'obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = np.linspace(0.0, 2*pi, num=nl, endpoint=False)
    v_range = np.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the M\'obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs(u/pi -1)**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs(u/pi -1)**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = index * pre_alpha + alpha0
        for v in v_range:
            nodes.append([
                scale * (r + v*cos(alpha)) * cos(u),
                scale * (r + v*cos(alpha)) * sin(u),
                flatness * scale * v*sin(alpha)
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1,  i*nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1])
    # close the geometry
    if index % 2 == 0:
        # Close the geometry upside up (even M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1])
            elems.append([(nl - 1)*nw + j, j, j + 1])
    else:
        # Close the geometry upside down (odd M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1])
            elems.append([(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)])

    return np.array(nodes), np.array(elems)


def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser(
        description='Construct a triangulation of the Möbius strip.'
        )

    parser.add_argument(
        'filename',
        metavar='file',
        type=str,
        help='file to be written to'
        )

    parser.add_argument(
        '--index', '-i',
        type=int,
        default=1,
        help='Möbius index, the number of twists (default: 1)'
        )

    parser.add_argument(
        '--num', '-n',
        nargs=2,
        type=int,
        default=(51, 11),
        help=('Number of discreitization points ' +
              'in length and width of the strip (default: 101, 21)')
        )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    import meshio

    args = _parse_options()

    # create the mesh
    points, cells = create_moebius_mesh(args.num, args.index)

    meshio.write(
            args.filename,
            points,
            {'triangle': cells}
            )
