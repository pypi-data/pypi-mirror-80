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

    required = ['Peaks_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'min_count', 'colat', 'degree']
    defaults = [15, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], 30, False, False]
    types = ['int', 'int', 'list', 'list',
             'int', 'bool', 'bool']
    return required, defaults, types, stat_type


def Peak_Loc(map, weights, ctx):
    """
    Calculates Peaks on a convergence map.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Peak abundance function, peak coordinates
    """

    # standard devaition of map
    sig = np.std(map[map > hp.pixelfunc.UNSEEN])

    ell = map.size

    # Exclude last element
    nside = hp.get_nside(map)
    ran = np.arange(ell - 1)

    temp = map[-1]
    map[-1] = hp.pixelfunc.UNSEEN

    peaks = np.zeros(0, dtype=np.int)

    # calculate all the neighbours, chunked (slow but slim memory)
    num_chunks = 2
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        edges = np.any(map[neighbours] == hp.pixelfunc.UNSEEN, axis=0)

        # Get Peak positions (maxima)
        ps = np.all(map[neighbours] < map[r], axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        ps = np.logical_and(ps, np.logical_not(edges))

        peaks = np.append(peaks, r[ps])

    # Last Value treatment
    map[-1] = temp
    n0 = hp.get_all_neighbours(nside, ell - 1)
    if (np.all(map[n0] < map[ell - 1])):
        peaks = np.append(peaks, ell - 1)
    n1 = np.reshape(hp.get_all_neighbours(nside, n0).T, (-1))
    peaks2 = np.all(np.reshape(map[n1], (-1, 8))
                    < map[n0].reshape((-1, 1)), axis=1)
    peaks2 = n0[peaks2]

    peaks = _select(n1, peaks, peaks2)

    peak_vals = map[peaks]
    peak_vals = peak_vals / sig
    peak_theta, peak_phi = hp.pixelfunc.pix2ang(ctx['NSIDE'], peaks)
    if not ctx['colat']:
        peak_theta = np.pi / 2. - peak_theta
    if ctx['degree']:
        peak_phi = np.degrees(peak_phi)
        peak_theta = np.degrees(peak_theta)

    # stacking
    peak_coords = np.hstack(
        (peak_phi.reshape(-1, 1), peak_theta.reshape(-1, 1),
         peak_vals.reshape(-1, 1)))
    peak_coords = np.vstack((peak_coords, [[-999., -999., -999.]]))

    return peak_coords


def _select(n, p1, p2):
    for i in n:
        if ((i in p1) and (i not in p2)):
            p1 = p1[p1 != i]
        if ((i in p2) and (i not in p1)):
            p1 = np.append(p1, i)
    return p1


def process(data, ctx, scale_to_unity=False):
    return data


def slice(ctx):
    return 1, 1, 'none', 1


def decide_binning_scheme(data, meta, bin, ctx):
    return [], []


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['Peaks_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Peaks_sliced_bins']
            f = np.asarray(f)
        filter = np.append(filter, f)
    return filter
