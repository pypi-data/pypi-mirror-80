
import healpy as hp

import HealpixMap as hmap

import numpy as np
from numpy import array, log2, sqrt

class HealpixBase:
    """
    Basic operations related to HEALPix pixelization, for which the map
    contents information is not needed. This class is conceptually very similar 
    the the Healpix_Base class of Healpix_cxx.

    Single resolution maps are fully defined by specifying their order 
    (or NSIDE) and ordering scheme ("RING" or "NESTED"). 

    Multi-resolution maps follow an explicit "NUNIQ" scheme, with each pixel 
    identfied by a _uniq_ number. No specific is needed nor guaranteed.

    .. warning::
        The initialization input is not validated by default. Consider calling 
        `is_mesh_valid()` after initialization, otherwise results might be
        unexpected.


    Args:
        uniq (array): Explicit numbering of each pixel in an "NUNIQ" scheme.
        order (int): Order of HEALPix map.
        nside (int): Alternatively, you can specify the NSIDE parameter.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
    """

    def __init__(self,
                 uniq = None,
                 order = None,
                 nside = None,
                 scheme = 'ring'):

        if uniq is not None:
            # MOC map

            self._uniq = uniq

            # Scheme and order are implicit
            self._scheme = "NUNIQ"
            
            self._order = hmap.uniq2order(max(uniq))
            
        else:
            # Single resolution map

            self._uniq = None
            
            # User specified nside instead of order
            if nside is not None:
                
                if order is not None:
                    raise ValueError("Specify either 'order' or 'nside'")
                
                order = hp.nside2order(nside)

            if order is None:
                raise ValueError("Specifcy nside or order")
                
            self._order = order

            if scheme is None:
                    raise ValueError("Specify scheme")

            self._scheme = scheme.upper()

            if self._scheme not in ['RING','NESTED', 'NUNIQ']:
                raise ValueError("Scheme can only be 'ring', 'nested' or 'NUNIQ'")


    def __eq__(self, other):

        if self.is_moc:
            return array_equal(self._uniq, other._uniq)
        else:
            return (self._order == other._order and 
                    self._scheme == other._scheme)
            
    def uniq(self, pix):
        """
        Get the UNIQ value of a pixel (as used in [])

        Args:
            pix (int or array): Pixel number

        Return:
            int
        """

        if self.is_moc:

            return self._uniq[pix]

        else:

            if not self.is_nested:
                pix = hp.ring2nest(self.nside, pix)
                
            return hmap.nest2uniq(self.nside, pix)
            
    @classmethod
    def adaptive_moc_mesh(cls, split_fun, max_order):
        """
        Return a MOC mesh with an adaptive resolution
        determined by an arbitrary function.

        Args:
            split_fun (function): This method should return ``True`` if a pixel 
            should be split into pixel of a higher order, and ``False`` otherwise. 
            It takes two integers, ``start`` (inclusive) and ``stop`` (exclusive), 
            which correspond to a single pixel in nested rangeset format for a 
            map of order ``max_order``.
            max_order (int): Maximum HEALPix order to consider

        Return:
            HealpixBase
        """

        map_uniq = array([], dtype = int)

        order_list = array(range(max_order+1))
        nside = 2**order_list
        npix_ratio = 4 ** (max_order - order_list)
        uniq_shift = 4 * nside * nside
        npix_ratio = 4 ** (max_order - order_list)

        start_buffer = np.zeros((max_order+1, 4), dtype=int)
        cursor = -np.ones((max_order+1), dtype=int)

        for base_pix in range(12):

            order = 0
            start_buffer[order][0] = base_pix * npix_ratio[order]
            cursor[order] = 0

            while order >= 0:

                if cursor[order] < 0:
                    order -= 1
                    continue

                start = start_buffer[order][cursor[order]]
                stop  = start + npix_ratio[order]

                cursor[order] -= 1

                if order < max_order and split_fun(start, stop):
                    # Split

                    order += 1

                    split_shift = array(range(4))*npix_ratio[order]
                    start_buffer[order] = start + split_shift

                    cursor[order] = 3

                else:
                    # Add to map

                    uniq = (start / npix_ratio[order] + uniq_shift[order]).astype(int) 

                    map_uniq = np.append(map_uniq, uniq)

        return cls(map_uniq)

    @classmethod
    def moc_from_pixels(cls, pixels, order, nest = False):
        """
        Return a MOC mesh where a list of pixels are kept at a 
        given order, and every other pixel is appropiately downsampled.
        
        Also see the more generic ``adaptive_moc()`` and ``adaptive_moc_mesh()``.

        Args:
            pixels (array): Pixels that must be kept at the finest pixelation
            order (int): Maximum healpix order (that is, the order for the pixel
                list)
            nest (bool): Whether the pixels are a 'NESTED' or 'RING' scheme
        """

        nside = hp.order2nside(order)

        # Always work in nested
        if not nest:
            pixels = array([hp.ring2nest(nside, pix) for pix in pixels])
            
        # Auxiliary function so we can reuse adaptive_moc_mesh()
        pixels.sort()
        
        def pix_list_range_intersect(start, stop):

            start_index,stop_index = np.searchsorted(pixels, [start,stop])

            return start_index < stop_index

        # Get the grid        
        return cls.adaptive_moc_mesh(pix_list_range_intersect, 
                                             order)

    def conformable(self, other):
        """
        For single-resolution maps, return ``True`` if both maps have the same
        order and scheme.

        For MOC maps, return `True` if both maps have the same list of UNIQ 
        pixels (including the ordering)
        """

        if self.scheme != other.scheme:
            return False
        
        if self.is_moc:

            return np.array_equal(self._uniq, other._uniq)

        else:

            return self.order == other.order

    @property
    def npix(self):
        """
        Get number of pixels.

        For multi-resolutions maps, this corresponds to the number of utilized 
        UNIQ pixels.

        Return:
            int
        """

        if self.is_moc:   
            return len(self._uniq)
        else:
            return int(12 * 4**self._order)

    @property
    def order(self):
        """
        Get map order

        Return:
            int
        """
        
        return self._order

    @property
    def nside(self):
        """
        Get map NSIDE

        Return:
            int
        """

        return int(2**self.order)
        
    @property
    def scheme(self):
        """
        Return HEALPix scheme
        
        Return:
            str: Either 'NESTED', 'RING' or 'NUNIQ'
        """

        return self._scheme

    @property
    def is_nested(self):
        """
        Return true if scheme is NESTED or NUNIQ
        
        Return
            bool
        """

        return self._scheme == "NESTED" or self._scheme == 'NUNIQ'
        
    @property
    def is_ring(self):
        """
        Return true if scheme is RING
        
        Return
            bool
        """

        return self._scheme == "RING"

    @property
    def is_moc(self):
        """
        Return true if this is a Multi-Dimensional Coverage (MOC) map 
        (multi-resolution)

        Return:
            bool
        """

        return self._uniq is not None

    def pix_rangesets(self, order):
        """
        Get the equivalent range of `child pixels` in nested scheme for a map 
        of a higher order

        Args:
            order (int): Order of output range sets

        Return:
            recarray: With columns named 'start' (inclusive) and 
                'stop' (exclusive) 
        """

        if self.scheme == 'NESTED':

            start,stop = hmap.nest2range(self.order, range(self.npix), order)

        elif self.scheme == 'RING':

            start,stop = hmap.nest2range(self.order,
                                         hp.ring2nest(self.nside, range(self.npix)),
                                         order)

        else:
            #self.scheme == 'NUNIQ'

            start,stop = hmap.uniq2range(self._uniq, order)

        return np.rec.fromarrays([start,stop], names = ['start', 'stop'])

    def pixarea(self, pix = 0):
        """
        Return area of pixel in steradians

        Args:
            pix (int or array): Pixel number. Only relevant for MOC maps
        
        Return:
            float or array
        """

        if self.is_moc:
            order = hmap.uniq2order(self._uniq[pix])
        else:
            order = self.order

        return 1.047197551196597746 / 4**order
        
    def pix2ang(self, pix):
        """
        Return the coordinates of the center of a pixel
        
        Args:
            pix (int or array)

        Return:
            (float or array, float or array)
        """

        if self.is_moc:

            pix,order = hmap.uniq2nest(self.pix2uniq(pix))

            nside = hp.order2nside(order)

            return hp.pix2ang(nside, pix, nest = True)
            
        else:
            return hp.pix2ang(self.nside, pix, nest = self.is_nested)
            
    def ang2pix(self, theta, phi):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            theta (float or array): Zenith angle
            phi (float or arrray): Azimuth angle
      
        Return:
            int or array
        """

        pixels = hp.ang2pix(self.nside, theta, phi, nest=self.is_nested)
        
        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
            
    def vec2pix(self, x, y, z):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            theta (float or array): Zenith angle
            phi (float or arrray): Azimuth angle
      
        Return:
            int or array
        """

        pixels = hp.vec2pix(self.nside, x, y, z, nest=self.is_nested)

        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
        
    def pix2uniq(self, ipix):
        """
        Get the UNIQ representation of a given pixel index.

        Args:
            ipix (int): Pixel number in the current scheme (as used for [])
        """

        if self.is_moc:

            return self._uniq[ipix]

        else:

            if self.scheme == 'RING':
                pix = hp.ring2nest(self.nside, pix)

            return hmap.nest2uniq(self.nside, pix)

    def nest2pix(self, pix):
        """
        Get the corresponding pixel in the current grid for a pixel in NESTED
        scheme. For MOC map, return the pixel that contains it. 

        Args:
            pix (int or array): Pixel number in NESTED scheme. Must correspond 
                to a map of the same order as the current.

        Return:
            int or array
        """

        if self.is_moc:

            # Work with rangesets for maximum order,
            # then find pixel number for this order,
            # and then find the rangesets that contain these pixels

            rangesets = self.pix_rangesets(self.order)
            
            rs_argsort = np.argsort(rangesets.stop)
            
            ipix = np.searchsorted(rangesets.stop, pix,
                                   side = 'right',
                                   sorter = rs_argsort)

            opix = rs_argsort[ipix]

            opix[pix == -1] = -1 # Follow healpy convention for null pix

            return opix
            
        else:
            
            if self.is_nested:
                return pix
            else:
                return hp.nest2ring(self.nside, pix)
            
    
    def get_interp_weights(self, theta, phi):
        """
        Return the 4 closest pixels on the two rings above and below the 
        location and corresponding weights. Weights are provided for bilinear 
        interpolation along latitude and longitude

        Args:
            theta (float or array): Zenith angle (rad)
            phi (float or array): Azimuth angle (rad)
 
        Return:
            tuple: (pixels, weights), each with of (4,) if the input is scalar,
                if (4,N) where N is size of
                theta and phi. For MOC maps, these pixel numbers might repeate.
        """

        pixels,weights = hp.get_interp_weights(self.nside, theta, phi,
                                               nest = self.is_nested)

        if self.is_moc:
            pixels = self.nest2pix(pixels)

        return (pixels, weights)
            
    def get_all_neighbours(self, theta, phi = None):
        """
        Return the 8 nearest pixels. For MOC maps, these might repeat, as this
        is equivalent to raterizing the maps to the highest order, getting the 
        neighbohrs, and then finding the pixels tha contain them.

        Args:
            theta (float or int or array): Zenith angle (rad). If phi is 
                ``None``, these are assummed to be pixels numbers. For MOC maps,
                these are assumed to be pixel numbers in NESTED scheme for the
                equivalent single-resolution map of the highest order.
            phi (float or array or None): Azimuth angle (rad)

        Return:
            array: pixel number of the SW, W, NW, N, NE, E, SE and S neighbours,
                shape is (8,) if input is scalar, otherwise shape is (8, N) if 
                input is of length N. If a neighbor does not exist (it can be 
                the case for W, N, E and S) the corresponding pixel number will 
                be -1.
        """
        
        neighbors = hp.get_all_neighbours(self.nside, theta, phi,
                                          nest = self.is_nested)

        print(neighbors)
        
        if self.is_moc:
            neighbors = self.nest2pix(neighbors)

        return neighbors
 
    def is_mesh_valid(self):
        """
        Return ``True`` is the map pixelization is valid. For
        single resolution this simply checks that the size is a valid NSIDE value.
        For MOC maps, it checks that every point in the sphere is covered by
        one and only one pixel.
        
        Return:
            True
        """

        if self.is_moc:

            # Work in rangesets, and check that there is no gap in between them
            rs = self.pix_rangesets(self.order)

            rs.sort(order = 'start')

            return (rs.start[0] == 0 and
                    rs.stop[-1] == hp.nside2npix(self.nside) and
                    np.array_equal(rs.start[1:], rs.stop[:-1]))
            
        else:
                
            return hp.isnpixok(self.npix)

    def _pix_query_fun(self, fun):
        """
        Return a wrapper for healpy's pix querying routines

        Args:
            fun (function): Healpy's query_* functions
        
        Return:
            function: With apprpiate grid, passes rest of arguments to fun
        """

        def wrapper(*args, **kwargs):

            if self.is_moc:

                # We'll do it order by order

                pix_per_order = [[] for _ in range(self.order+1)]
                nest_pix_per_order = [[] for _ in range(self.order+1)]

                for pix in range(self.npix):

                    nest_pix,order = hmap.uniq2nest(self.uniq(pix))

                    pix_per_order[order].append(pix)
                    nest_pix_per_order[order].append(nest_pix)

                query_pix = np.zeros(0, dtype = int)

                for order in range(self.order+1):

                    pixels = fun(hp.order2nside(order), nest = True,
                                 *args, **kwargs)

                    query_bool = np.isin(nest_pix_per_order[order], pixels)

                    order_pix = array(pix_per_order[order], dtype=int)

                    query_pix = np.append(query_pix,
                                          order_pix[query_bool])

                return query_pix
                        
            else:

                return fun(self.nside, nest = self.is_nested,
                           *args, **kwargs)

        return wrapper                

    def query_polygon(self, vertices, inclusive=False, fact=4):
        """
        Returns the pixels whose centers lie within the convex polygon defined 
        by the vertices array (if inclusive is False), or which overlap with 
        this polygon (if inclusive is True).

        Args:
            vertices (float): Vertex array containing the vertices of the 
                polygon, shape (N, 3).
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
            
        Return:
            int array: The pixels which lie within the given polygon.
        """
        
        fun = self._pix_query_fun(hp.query_polygon)

        return fun(vertices, inclusive=inclusive, fact=fact)

    def query_disc(self, vec, radius, inclusive=False, fact=4):
        """

        Args:
            vec (float, sequence of 3 elements): The coordinates of unit vector 
                defining the disk center.
            radius (float): The radius (in radians) of the disk
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
        
        Return:
            int array: The pixels which lie within the given disc.
        """
        
        fun = self._pix_query_fun(hp.query_disc)

        return fun(vec, radius, inclusive=inclusive, fact=fact)

    def query_strip(self,  theta1, theta2, inclusive=False):
        """
        Returns pixels whose centers lie within the colatitude range defined by 
        theta1 and theta2 (if inclusive is False), or which overlap with this 
        region (if inclusive is True). If theta1<theta2, the region between 
        both angles is considered, otherwise the regions 0<theta<theta2 and 
        theta1<theta<pi.

        Args:
            theta (float): First colatitude (radians)
            phi (float): Second colatitude (radians)
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.

        Return:
            int array: The pixels which lie within the given strip.
        """
        
        fun = self._pix_query_fun(hp.query_strip)

        return fun(theta1, theta2, inclusive=inclusive)
    
    def boundaries(self, pix, step = 1):
        """
        Returns an array containing vectors to the boundary of the nominated pixel.

        The returned array has shape (3, 4*step), the elements of which are the 
        x,y,z positions on the unit sphere of the pixel boundary. In order to 
        get vector positions for just the corners, specify step=1.
        """
        
        if self.is_moc:

            def single_pix_bounds(pix):

                nest_pix, order = hmap.uniq2nest(self._uniq[pix])
    
                nside = hp.order2nside(order)
    
                return hp.boundaries(nside, nest_pix, step = step, nest = True)

            moc_bounds = np.vectorize(single_pix_bounds)
            
            return moc_bounds(pix)

        else:

            return hp.boundaries(self.nside, pix, step, nest = self.is_nested)

    
        
