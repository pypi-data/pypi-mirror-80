# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
from estats import summary


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['Voids_max', 'Voids_min', 'Voids_steps',
                'void_upper_threshold', 'Voids_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'min_count']
    defaults = [0.05, -0.3, 1000, -2.5, 15, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], 30]
    types = ['float', 'float', 'int', 'float', 'int', 'int', 'list', 'list',
             'int']
    return required, defaults, types, stat_type


def Voids(map, weights, ctx):
    """
    Calculates Voids on a convergence map.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Void abundance function, void coordinates
    """

    # standard devaition of map
    sig = np.std(map[map > hp.pixelfunc.UNSEEN])

    ell = map.size

    # Exclude last element
    nside = hp.get_nside(map)
    ran = np.arange(ell - 1)

    temp = map[-1]
    map[-1] = hp.pixelfunc.UNSEEN

    voids = np.zeros(0, dtype=np.int)

    # calculate all the neighbours, chunked (slow but slim memory)
    num_chunks = 2
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        edges = np.any(map[neighbours] == hp.pixelfunc.UNSEEN, axis=0)

        # Get Peak positions (maxima)
        vs = np.all(map[neighbours] > map[r], axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        vs = np.logical_and(vs, np.logical_not(edges))

        voids = np.append(voids, r[vs])

    # Last Value treatment
    map[-1] = temp
    n0 = hp.get_all_neighbours(nside, ell - 1)
    if (np.all(map[n0] < map[ell - 1])):
        voids = np.append(voids, ell - 1)
    n1 = np.reshape(hp.get_all_neighbours(nside, n0).T, (-1))
    voids2 = np.all(np.reshape(map[n1], (-1, 8))
                    > map[n0].reshape((-1, 1)), axis=1)
    voids2 = n0[voids2]

    voids = _select(n1, voids, voids2)

    # Remove UNSEENS labeled as Voids
    valids = map[voids] > -1e+20
    if len(valids) > 0:
        voids = voids[valids]

    # get values
    # and cutting off below threshold coordinates
    void_vals = map[voids]
    voids_pixels = voids[void_vals / sig <= ctx['void_upper_threshold']]
    void_theta, void_phi = hp.pixelfunc.pix2ang(
        ctx['NSIDE'], voids_pixels, lonlat=True)

    # stacking
    void_coords = np.hstack(
        (void_phi.reshape(-1, 1), void_theta.reshape(-1, 1)))

    # adding separator
    void_coords = np.vstack((void_coords, np.asarray([[-999., -999.]])))

    # Binning for values
    void_bins = np.linspace(
        ctx['Voids_min'], ctx['Voids_max'], ctx['Voids_steps'] - 1)
    void_bins = np.hstack((-np.inf, void_bins, np.inf))

    void_vals = np.histogram(void_vals, bins=void_bins)[0]
    void_vals = void_vals.reshape(1, void_vals.size)

    return (void_vals, void_coords)


def _select(n, p1, p2):
    for i in n:
        if ((i in p1) and (i not in p2)):
            p1 = p1[p1 != i]
        if ((i in p2) and (i not in p1)):
            p1 = np.append(p1, i)
    return p1


def process(data, ctx, scale_to_unity=False):
    num_of_scales = len(ctx['scales'])

    new_data = np.zeros(
        (int(data.shape[0] / num_of_scales), data.shape[1]
         * num_of_scales))
    for jj in range(int(data.shape[0] / num_of_scales)):
        new_data[jj, :] = data[jj * num_of_scales:
                               (jj + 1) * num_of_scales, :].ravel()
    return new_data


def slice(ctx):
    # number of datavectors for each scale
    mult = 1
    # number of scales
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'sum'

    n_bins_sliced = ctx['Voids_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # For Abundance function perform equal width
    # splitting but require a minum
    # count of objects in each bin for every realisation
    # (requires loading all files)

    range_edges = [ctx['Voids_min'], ctx['Voids_max']]
    n_bins_original = ctx['Voids_steps']
    num_of_scales = len(ctx['scales'])
    n_bins_sliced = ctx['Voids_sliced_bins']
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    bin_idx = np.zeros(meta.shape[0], dtype=bool)
    bin_idx[np.where(meta[:, 0] == bin)[0]] = True
    bin_idx = np.repeat(bin_idx, meta[:, 1].astype(int))
    data = data[bin_idx, :]

    # Get bins for each smooting scale
    for scale in range(num_of_scales):
        # get lower bound for bins
        min_bin = summary._get_border(
            data[:, n_bins_original * scale:
                 n_bins_original * (scale + 1)], ctx['min_count'])
        # get upper bound for bins
        max_bin = summary._get_border(
            np.flip(data[:, n_bins_original * scale:
                         n_bins_original * (scale + 1)], axis=1),
            ctx['min_count'])
        max_bin = n_bins_original - max_bin

        # equal width splitting of remaining bins in between
        n_bins_left = max_bin - min_bin
        remain = n_bins_left % (n_bins_sliced - 2)
        remain_front = remain // 2
        remain_back = remain_front + remain % 2

        min_bin += remain_front
        max_bin -= remain_back

        # Get bin edge indices
        bin_edge_indices_temp = np.linspace(
            min_bin, max_bin, num=n_bins_sliced - 1)

        bin_edge_indices_temp = bin_edge_indices_temp.astype(int)

        bin_edge_indices[scale, 0] = 0
        bin_edge_indices[scale, -1] = n_bins_original

        bin_edge_indices[scale, 1:-1] = bin_edge_indices_temp

        # get original bin center values (except first and last bin)
        kappa_range = np.linspace(
            range_edges[0], range_edges[1], n_bins_original - 1)
        kappa_range += 0.5 * (kappa_range[1] - kappa_range[0])

        for jj in range(1, bin_edge_indices.shape[1] - 2):
            bin_centers[scale, jj] = np.nanmean(kappa_range[int(
                bin_edge_indices[scale, jj] - 1):
                int(bin_edge_indices[scale, jj + 1] - 1)])
        bin_centers[scale, 0] = bin_centers[scale, 1] - \
            (bin_centers[scale, 2] - bin_centers[scale, 1])
        bin_centers[scale, -1] = bin_centers[scale, -2] + \
            (bin_centers[scale, -2] - bin_centers[scale, -3])

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['Voids_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Voids_sliced_bins']
            f = np.asarray(f)
        filter = np.append(filter, f)
    return filter
