# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# check if ECl is available
import numpy as np
ECl_avail = True
try:
    import ECl
except ImportError:
    ECl_avail = False
    import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'convergence'

    required = ['lmax', 'CLs_sliced_bins', 'CLs_min', 'CLs_max']
    defaults = [1000, 20, 100, 1000]
    types = ['int', 'int', 'int', 'int']
    return required, defaults, types, stat_type


def CLs(map, weights, ctx):
    """
    Calculates the Angular Power spectrum on a convergence map.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights (integer >=0)
    :param ctx: Context instance
    :return: TT-cls
    """

    lmax = ctx['lmax'] - 1

    # check if weights are set
    if len(weights) == 0:
        print("No weight map found. Using equal weights for each pixel")
        weights = np.ones_like(map, dtype=ctx['prec'])

    if ECl_avail:
        cls = ECl.run_anafast.run_anafast(
            map, map_1_type='s0', lmax=lmax, weights_1=weights)['cl_TT']
    else:
        # proper weight masking
        select_seen = weights > 0
        select_unseen = ~select_seen
        select_unseen |= map == hp.UNSEEN

        # weighting
        map = (map * weights).astype(np.float)
        map[select_unseen] = hp.UNSEEN

        cls = hp.sphtfunc.anafast(map, lmax=lmax)

    cls = cls.reshape(1, cls.size)

    return cls


def process(data, ctx, scale_to_unity=False):
    if scale_to_unity:
        data *= 1e4
    return data


def slice(ctx):
    # number of datavectors for each scale
    mult = 1
    # number of scales
    num_of_scales = 1
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    n_bins_sliced = ctx['CLs_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # Perform simple equal width splitting for Cls.

    range_edges = [ctx['CLs_min'], ctx['CLs_max']]
    num_of_scales = 1
    n_bins_sliced = ctx['CLs_sliced_bins']
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    # Cut out desired l range
    minimum = range_edges[0]
    maximum = range_edges[1]
    diff = maximum - minimum

    per_bin = diff // n_bins_sliced
    remain = diff % n_bins_sliced
    remain_front = remain // 2
    remain_back = remain_front + remain % 2

    # Decide on edge indices
    bin_edge_indices_temp = np.arange(
        remain_front + minimum, maximum - remain_back, per_bin)
    bin_edge_indices_temp[0] -= remain_front
    bin_edge_indices_temp = np.append(bin_edge_indices_temp, maximum)

    # Decide on central bin values
    bin_centers_temp = np.zeros(0)
    for jj in range(len(bin_edge_indices_temp) - 1):
        bin_centers_temp = np.append(
            bin_centers_temp,
            np.nanmean(bin_edge_indices_temp[jj:jj + 2]))

    # For consistency with other binning scheme
    # assign same binning to all scales
    for scale in range(num_of_scales):
        bin_centers[scale, :] = bin_centers_temp
        bin_edge_indices[scale, :] = bin_edge_indices_temp

    return bin_edge_indices, bin_centers


def filter(ctx):
    return [True] * ctx['CLs_sliced_bins']
