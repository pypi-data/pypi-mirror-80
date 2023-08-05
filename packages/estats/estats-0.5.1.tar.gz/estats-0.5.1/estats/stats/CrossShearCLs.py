# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# check if ECl is available
import numpy as np
try:
    from ECl.run_anafast import run_anafast
    from ECl.run_polspice import run_polspice
except ImportError:
    raise Exception("Did not find ECl module")


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'shear'

    required = ['lmax', 'CrossShearCLs_sliced_bins', 'CrossShearCLs_min',
                'CrossShearCLs_max', 'cl_engine']
    defaults = [1000, 20, 100, 1000, 'anafast']
    types = ['int', 'int', 'int', 'int', 'str']
    return required, defaults, types, stat_type


def CrossShearCLs(map_1, map_2, map_1_sec, map_2_sec, weight_map_1,
                  weight_map_2, ctx):

    shear_map_1 = [map_1, map_2]
    shear_map_2 = [map_1_sec, map_2_sec]

    lmax = ctx['lmax'] - 1

    # check if weights are set
    if len(weight_map_1) == 0:
        print(
            "No sceondary weight map found. "
            "Using equal weights for each pixel")
        weight_map_1 = np.ones_like(map_1, dtype=ctx['prec'])
    if len(weight_map_2) == 0:
        print(
            "No sceondary weight map found. "
            "Using equal weights for each pixel")
        weight_map_2 = np.ones_like(map_1_sec, dtype=ctx['prec'])

    map_1_type = 's2'
    map_2_type = 's2'

    if ctx['cl_engine'] == 'anafast':
        Cl = run_anafast(shear_map_1, map_1_type,
                         map_2=shear_map_2,
                         map_2_type=map_2_type,
                         weights_1=weight_map_1,
                         weights_2=weight_map_2, lmax=lmax)
    elif ctx['cl_engine'] == 'polspice':
        Cl = run_polspice(shear_map_1, map_1_type,
                          map_2=shear_map_2,
                          map_2_type=map_2_type,
                          weights_1=weight_map_1,
                          weights_2=weight_map_2)
    else:
        raise Exception("Unknown cl_engine {}".format(ctx['cl_engine']))

    Cl_EE = Cl['cl_EE']
    Cl_EE = Cl_EE.reshape(1, Cl_EE.size)
    Cl_BB = Cl['cl_BB']
    Cl_BB = Cl_BB.reshape(1, Cl_BB.size)
    return (Cl_EE, Cl_BB)


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

    n_bins_sliced = ctx['CrossShearCLs_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # Perform simple equal width splitting for Cls.

    range_edges = [ctx['CrossShearCLs_min'], ctx['CrossShearCLs_max']]
    num_of_scales = 1
    n_bins_sliced = ctx['CrossShearCLs_sliced_bins']
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
    return [True] * ctx['CrossShearCLs_sliced_bins']
