# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# check if ECl is available
import numpy as np
try:
    import ECl
except ImportError:
    raise Exception("Did not find ECl module")


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'shear'

    required = ['lmax', 'ShearCLs_sliced_bins', 'ShearCLs_min', 'ShearCLs_max']
    defaults = [1000, 20, 100, 1000]
    types = ['int', 'int', 'int', 'int']
    return required, defaults, types, stat_type


def ShearCLs(map_1, map_2, weights, ctx):
    """
    Calculates Angular Power spectrum on shear maps (E and B modes).
    :param map_1: A Healpix shear map for first component
    :param map_2: A Healpix shear map for second component
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: E and B mode Shear cls
    """

    lmax = ctx['lmax'] - 1

    # check if weights are set
    if len(weights) == 0:
        print("No weight map found. Using equal weights for each pixel")
        weights = np.ones_like(map, dtype=ctx['prec'])

    cl_eb_full = ECl.run_anafast.run_anafast(
        (map_1, map_2), 's2', lmax=lmax)
    cls = cl_eb_full['cl_EE']
    cls = cls.reshape(1, cls.size)
    cls_B = cl_eb_full['cl_BB']
    cls_B = cls_B.reshape(1, cls_B.size)

    return (cls, cls_B)


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

    n_bins_sliced = ctx['ShearCLs_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # Perform simple equal width splitting for Cls.

    range_edges = [ctx['ShearCLs_min'], ctx['ShearCLs_max']]
    num_of_scales = 1
    n_bins_sliced = ctx['ShearCLs_sliced_bins']
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
    return [True] * ctx['ShearCLs_sliced_bins']
