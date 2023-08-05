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

    required = ['Minkowski_max', 'Minkowski_min', 'Minkowski_steps',
                'Minkowski_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'no_V0']
    defaults = [2.0, -2.0, 100, 16, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], False]
    types = ['float', 'float', 'int', 'int', 'int', 'list', 'list', 'bool']
    return required, defaults, types, stat_type


def Minkowski(kappa, weights, ctx):
    """
    Calculates Minkowski functionals on a convergence map.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Minkowski functionals as V0,V1,V2 concatinated.
    """

    # check context variables
    requires = ['Minkowski_max', 'Minkowski_min', 'Minkowski_steps']
    for parameter in requires:
        if parameter not in ctx:
            raise ValueError(
                "The keyword {} is not in the context".format(parameter))

    thresholds = np.linspace(ctx['Minkowski_min'],
                             ctx['Minkowski_max'], ctx['Minkowski_steps'])

    # gets the Minkowski functionals from a convergence map
    # weights for neighbors
    phi_weights = np.asarray([0, -1., 0., 0., 0., 1., 0., 0.]).reshape(8, 1)
    theta_weights = np.asarray([0, 0., 0., 1., 0., 0., 0., -1.]).reshape(8, 1)

    ell = kappa.size
    nside = hp.get_nside(kappa)
    ran = np.arange(ell, dtype=np.int)

    V1_tot = np.zeros(ell)
    V2_tot = np.zeros(ell)
    to_keep = np.zeros(ell, dtype=bool)
    num_chunks = 5
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        deriv_phi = np.zeros(ell)
        deriv_theta = np.zeros(ell)
        deriv_phi[r] = np.mean(
            (kappa[neighbours] - kappa[r]) * phi_weights, axis=0)
        deriv_theta[r] = np.mean(
            (kappa[neighbours] - kappa[r]) * theta_weights, axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        edges = np.any(kappa[neighbours] < -1e20, axis=0)
        to_keep_edges = np.logical_not(edges)

        # calculate V2 part by part to save RAM
        #######################################
        # term 1
        deriv_phi_theta = np.zeros(ell)
        deriv_phi_theta[r] = np.mean(
            (deriv_phi[neighbours] - deriv_phi[r]) * theta_weights, axis=0)
        V2 = 2. * deriv_phi * deriv_phi_theta
        V2 *= deriv_theta

        # term 2
        deriv_theta_theta = np.zeros(ell)
        deriv_theta_theta[r] = np.mean(
            (deriv_theta[neighbours] - deriv_theta[r]) * theta_weights, axis=0)
        V2 -= deriv_phi**2. * deriv_theta_theta

        # term 3
        deriv_phi_phi = np.zeros(ell)
        deriv_phi_phi[r] = np.mean(
            (deriv_phi[neighbours] - deriv_phi[r]) * phi_weights, axis=0)
        V2 -= deriv_theta**2. * deriv_phi_phi

        # remove extreme derivatives
        to_keep1 = np.abs(deriv_phi_phi) < 1e10
        to_keep2 = np.abs(deriv_phi_theta) < 1e10
        to_keep3 = np.abs(deriv_theta_theta) < 1e10

        to_keep_ext = np.logical_and(
            np.logical_and(to_keep1, to_keep2), to_keep3)
        to_keep[r] = np.logical_and(to_keep_ext[r], to_keep_edges)

        # calculate V1
        ##############
        V1 = deriv_theta**2. + deriv_phi**2.

        V2 /= V1
        V1 = np.sqrt(V1)
        V1_tot[r] = V1[r]
        V2_tot[r] = V2[r]

    # masking
    kappa = kappa[to_keep]
    V1 = V1_tot[to_keep]
    V2 = V2_tot[to_keep]

    # averaged standard deviation and normalization
    sigma_0 = np.sqrt(np.mean(kappa**2.))
    thresholds *= sigma_0
    denom = np.sum(kappa > -1e20)

    # Minkowski calculation
    res = np.zeros(0)
    for thres in thresholds:
        # calc the three MFs
        delta_func = np.isclose(kappa, thres, rtol=0.0, atol=1e-6)
        V0_ = np.sum(kappa >= thres) / denom
        V1_ = np.sum(V1[delta_func]) / (4. * denom)
        V2_ = np.sum(V2[delta_func]) / (2. * np.pi * denom)
        res = np.append(res, [V0_, V1_, V2_])

    # reordering
    V0 = res[0::3]
    V1 = res[1::3]
    V2 = res[2::3]
    res = np.append(V0, np.append(V1, V2))

    return res


def process(data, ctx, scale_to_unity=False):
    if scale_to_unity:
        data *= 1e10

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
    mult = 3
    # number of scales
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    n_bins_sliced = ctx['Minkowski_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # For Minkowski perform simple equal bin width splitting.
    # Same splitting for each smoothing scale.
    range_edges = [ctx['Minkowski_min'], ctx['Minkowski_max']]
    n_bins_original = ctx['Minkowski_steps']
    num_of_scales = len(ctx['scales'])
    n_bins_sliced = ctx['Minkowski_sliced_bins']
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    orig_bin_values = np.linspace(
        range_edges[0], range_edges[1], n_bins_original)

    per_bin = n_bins_original // n_bins_sliced
    remain = n_bins_original % n_bins_sliced
    remain_front = remain // 2
    remain_back = remain_front + remain % 2

    # Get edge indices
    bin_edge_indices_temp = np.arange(
        remain_front, n_bins_original - remain_back, per_bin)
    bin_edge_indices_temp[0] -= remain_front
    bin_edge_indices_temp = np.append(
        bin_edge_indices_temp, n_bins_original)

    # Get bin central values
    bin_centers_temp = np.zeros(0)
    for jj in range(len(bin_edge_indices_temp) - 1):
        bin_centers_temp = np.append(bin_centers_temp, np.nanmean(
            orig_bin_values[bin_edge_indices_temp[jj]:
                            bin_edge_indices_temp[jj + 1]]))

    # Assign splitting to each scale
    for scale in range(num_of_scales):
        bin_centers[scale, :] = bin_centers_temp
        bin_edge_indices[scale, :] = bin_edge_indices_temp

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)

        f = np.tile(f, 3)
        if ctx['no_V0']:
            f[:ctx['Minkowski_sliced_bins']] = False
        filter = np.append(filter, f)
    return filter
