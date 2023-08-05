# Pixelization related function for multi-order coverage maps
# See http://ivoa.net/documents/MOC

import numpy as np
from numpy import array, log2, sqrt, exp

def uniq2order(uniq):
    """
    Extract the corresponding order from a UNIQ numbered pixel

    Args:
        uniq (int or array): Pixel number

    Return:
        int or array: order
    """

    return (log2(array(uniq)/4)/2).astype(int)

def uniq2nest(uniq):
    """
    Convert from UNIQ ordering scheme to NESTED

    Args:
        uniq (int or array): Pixel number

    Return
        (int or array, int or array): npix,order
    """

    uniq = array(uniq)

    order = uniq2order(uniq)
    npix = uniq - 4 * (4**order)

    return npix,order

def nest2uniq(nside, ipix):
    """
    Convert from from NESTED to UNIQ scheme

    Args:
        nside (int): HEALPix NSIDE parameter
        ipix (int or array): Pixel number in NESTED scheme

    Return:
        int or array
    """

    ipix = array(ipix)

    return 4 * nside * nside + ipix

def nest2range(order_input, pix, order_output):
    """
    Get the equivalent range of pixel that correspond to all
    `child pixels` of a map of a greater order.

    Args:
        order_input (int or array): Order of input pixel
        pix (int or array): Input pixel.
        order_output (int): Order of map with `child pixels`

    Return:
        (int or array, int or array): Start pixel (inclusive) and 
            stop pixel (exclusive) 
    """

    if np.any(order_input > order_output):
        raise ValueError("Input order must be greater or equal to output order")

    npix_ratio = 4 ** (order_output - order_input)

    pix = array(pix)

    return (pix*npix_ratio, (pix+1)*npix_ratio)


def uniq2range(uniq, order):
    """
    Convert from a pixel number in NUNIQ scheme to the range of children 
    pixels that it would correspond to in a NESTED map of a given order

    Args:
       uniq (int or array): Pixel number in NUNIQ scheme
       order (int): Order of equivalent single resolution map

    Return:
        (int or array, int or array): Start pixel (inclusive) and 
            stop pixel (exclusive) 
    """

    pix,pix_order = uniq2nest(uniq)

    return nest2range(pix_order, pix, order)

def range2uniq(order, pix_range):
    """
    Convert from range of children pixels in a NESTED map of a given order
    to the corresponding uniq pixel number.

    Args:
        order (int): Order of equivalent single resolution map
        pix_range (int or array, int or array): Star pixel (inclusive) and 
            stop pixel (exclusive)

    Return:
        int
    """

    npix_ratio = array(pix_range[1]) - array(pix_range[0])

    nside = 2**order / sqrt(npix_ratio)

    pix = array(pix_range[0]) / npix_ratio

    if (nside < 1 or
        any([not float(i).is_integer() for i in array([nside]).flatten()]) or
        any([not float(i).is_integer() for i in array([pix]).flatten()])):
        raise ValueError("pix_range is malformed for a HEALPix "
                         "map of order {}".format(order))

    return nest2uniq(array(nside).astype(int),
                                 array(pix).astype(int))

