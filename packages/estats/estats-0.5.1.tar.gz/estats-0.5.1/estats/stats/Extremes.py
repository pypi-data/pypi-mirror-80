# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['Peaks_max', 'Peaks_min', 'Peaks_steps',
                'peak_lower_threshold', 'Peaks_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'min_count',
                'Voids_max', 'Voids_min', 'Voids_steps',
                'void_upper_threshold', 'Voids_sliced_bins']

    defaults = [0.3, -0.05, 1000, 2.5, 15, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], 30,
                0.05, -0.3, 1000, -2.5, 15]
    types = ['float', 'float', 'int', 'float', 'int', 'int',
             'list', 'list', 'int', 'float', 'float', 'int', 'float', 'int']
    return required, defaults, types, stat_type


def Extremes(map, weights, ctx):
    """
    Calculates Peaks and Voids on a convergence map. Same as running Peaks
    and Voids separately but faster.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Peak abundance function, peak coordinates,
    void abundance function, void coordinates
    """
    # check context variables
    requires = ['Peaks_max', 'Peaks_min', 'Peaks_steps',
                'Voids_max', 'Voids_min', 'Voids_steps',
                'peak_lower_threshold', 'void_upper_threshold', 'NSIDE']
    for parameter in requires:
        if parameter not in ctx:
            raise ValueError(
                "The keyword {} is not in the context".format(parameter))

    # standard devaition of map
    sig = np.std(map[map > hp.pixelfunc.UNSEEN])

    ell = map.size

    # Exclude last element
    nside = hp.get_nside(map)
    ran = np.arange(ell - 1)

    temp = map[-1]
    map[-1] = hp.pixelfunc.UNSEEN

    peaks = np.zeros(0, dtype=np.int)
    voids = np.zeros(0, dtype=np.int)

    # calculate all the neighbours, chunked (slow but slim memory)
    num_chunks = 2
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        edges = np.any(map[neighbours] == hp.pixelfunc.UNSEEN, axis=0)

        # Get Peak positions (maxima)
        ps = np.all(map[neighbours] < map[r], axis=0)
        vs = np.all(map[neighbours] > map[r], axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        ps = np.logical_and(ps, np.logical_not(edges))
        vs = np.logical_and(vs, np.logical_not(edges))

        peaks = np.append(peaks, r[ps])
        voids = np.append(voids, r[vs])

    # Last Value treatment
    map[-1] = temp
    n0 = hp.get_all_neighbours(nside, ell - 1)
    if (np.all(map[n0] < map[ell - 1])):
        peaks = np.append(peaks, ell - 1)
        voids = np.append(voids, ell - 1)
    n1 = np.reshape(hp.get_all_neighbours(nside, n0).T, (-1))
    peaks2 = np.all(np.reshape(map[n1], (-1, 8))
                    < map[n0].reshape((-1, 1)), axis=1)
    voids2 = np.all(np.reshape(map[n1], (-1, 8))
                    > map[n0].reshape((-1, 1)), axis=1)
    peaks2 = n0[peaks2]
    voids2 = n0[voids2]

    peaks = _select(n1, peaks, peaks2)
    voids = _select(n1, voids, voids2)

    # Remove UNSEENS labeled as Voids
    valids = map[voids] > -1e+20
    if len(valids) > 0:
        voids = voids[valids]

    # get values
    # and cutting off below threshold coordinates
    peak_vals = map[peaks]
    peaks_pixels = peaks[peak_vals / sig >= ctx['peak_lower_threshold']]
    peak_theta, peak_phi = hp.pixelfunc.pix2ang(
        ctx['NSIDE'], peaks_pixels, lonlat=True)

    void_vals = map[voids]
    voids_pixels = voids[void_vals / sig <= ctx['void_upper_threshold']]
    void_theta, void_phi = hp.pixelfunc.pix2ang(
        ctx['NSIDE'], voids_pixels, lonlat=True)

    # stacking
    peak_coords = np.hstack(
        (peak_phi.reshape(-1, 1), peak_theta.reshape(-1, 1)))
    void_coords = np.hstack(
        (void_phi.reshape(-1, 1), void_theta.reshape(-1, 1)))

    # adding separator
    peak_coords = np.vstack((peak_coords, np.asarray([[-999., -999.]])))
    void_coords = np.vstack((void_coords, np.asarray([[-999., -999.]])))

    # Binning for values
    peak_bins = np.linspace(
        ctx['Peaks_min'], ctx['Peaks_max'], ctx['Peaks_steps'] - 1)
    peak_bins = np.hstack((-np.inf, peak_bins, np.inf))
    void_bins = np.linspace(
        ctx['Voids_min'], ctx['Voids_max'], ctx['Voids_steps'] - 1)
    void_bins = np.hstack((-np.inf, void_bins, np.inf))

    peak_vals = np.histogram(peak_vals, bins=peak_bins)[0]
    peak_vals = peak_vals.reshape(1, peak_vals.size)

    void_vals = np.histogram(void_vals, bins=void_bins)[0]
    void_vals = void_vals.reshape(1, void_vals.size)

    return (peak_vals, peak_coords, void_vals, void_coords)


def _select(n, p1, p2):
    for i in n:
        if ((i in p1) and (i not in p2)):
            p1 = p1[p1 != i]
        if ((i in p2) and (i not in p1)):
            p1 = np.append(p1, i)
    return p1
