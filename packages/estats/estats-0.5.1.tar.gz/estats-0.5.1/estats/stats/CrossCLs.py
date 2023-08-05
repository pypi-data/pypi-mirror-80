# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
from ekit.logger import vprint
try:
    import ECl
except ImportError:
    raise Exception("Did not find ECl module")


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'convergence'

    required = ['lmax', 'CrossCLs_sliced_bins', 'CrossCLs_min',
                'CrossCLs_max', 'n_tomo_bins']
    defaults = [1000, 20, 100, 1000, 4]
    types = ['int', 'int', 'int', 'int', 'int']
    return required, defaults, types, stat_type


def CrossCLs(map1, map2, weights1, weights2, ctx):
    """
    Calculates the Cross Angular Power spectrum of two convergence maps.
    :param map1: A Healpix convergence map
    :param map2: A second Healpix convergence map
    :param weights1: A Healpix map with pixel weights
    :param weights2: A second Healpix map with pixel weights
    :param ctx: Context instance
    :return: Cross CLs
    """
    lmax = ctx['lmax'] - 1

    # check if weights are set
    if len(weights1) == 0:
        vprint("No weight1 map found. Using equal weights for each pixel")
        weights1 = np.ones_like(map, dtype=ctx['prec'])
    if len(weights2) == 0:
        vprint("No weight2 map found. Using equal weights for each pixel")
        weights2 = np.ones_like(map, dtype=ctx['prec'])

    cls = ECl.run_anafast.run_anafast(
        map_1=map1, map_1_type='s0', map_2=map2, map_2_type='s0',
        weights_1=weights1, weights_2=weights2, lmax=lmax)['cl_TT']

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

    range_edges = [ctx['CrossCLs_min'], ctx['CrossCLs_max']]
    num_of_scales = 1
    n_bins_sliced = ctx['CrossCLs_sliced_bins']
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
    return [True] * ctx['CrossCLs_sliced_bins']
