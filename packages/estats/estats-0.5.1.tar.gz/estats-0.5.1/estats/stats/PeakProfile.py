# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Nicole Leemann, adapted by Dominik Zuercher

import numpy as np
import healpy as hp
from scipy import stats
import importlib


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['scale', 'NSIDE', 'PeakProfile_bins',
                'Peaks_max', 'Peaks_min', 'Peaks_steps',
                'peak_lower_threshold',
                'scales', 'selected_scales']
    defaults = [21.1, 1024, 10, 0.3, -0.05, 1000, 2.5,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                    15.8, 13.2, 10.5, 7.9, 5.3, 2.6],
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2, 10.5]]
    types = ['float', 'int', 'int', 'float',
             'float', 'int', 'float', 'list', 'list']
    return required, defaults, types, stat_type


def rad2deg(theta):
    # convert radians to degrees
    return (theta / np.pi * 180) % 360


def deg2rad(theta):
    # convert degrees to radians
    return theta / 180. * np.pi


def arcmin2rad(theta):
    # convert arcminutes to radians
    return deg2rad(theta / 60)


def rad2arcmin(theta):
    # convert radians to arcminutes
    return rad2deg(theta) * 60


def binned_profile(kappa, nside, fwhm, bins, peak_pos_theta, peak_pos_phi,
                   ctx):
    cen_pix = hp.pixelfunc.ang2pix(nside, peak_pos_theta, peak_pos_phi)
    cen_val = kappa[cen_pix]
    cen_vec = hp.pixelfunc.pix2vec(nside, cen_pix)

    # get pixels around peak. Search up to 1.25 times the scale
    # (convert arcmin -> deg -> radians)
    radius = arcmin2rad(5. / 4. * fwhm)
    disc_pix = hp.query_disc(nside, cen_vec, radius)
    disc_val = kappa[disc_pix]

    # deal with edges
    idx = disc_val > hp.UNSEEN
    disc_val = disc_val[idx]
    disc_pix = disc_pix[idx]

    # get relative pixel values
    disc_val /= cen_val

    # get distances to central pixel in arcmin
    disc_ang = hp.pixelfunc.pix2ang(nside, disc_pix)
    disc_th = disc_ang[0]
    disc_ph = disc_ang[1]

    dth = disc_th - peak_pos_theta
    dph = disc_ph - peak_pos_phi
    disc_r = np.sqrt(dth ** 2 + dph ** 2)
    disc_r = rad2arcmin(disc_r)  # in arcmin

    # bin pixels
    bin_means = stats.binned_statistic(
        disc_r, disc_val, statistic='mean', bins=bins)[0]
    bin_std, edges, nums = stats.binned_statistic(
        disc_r, disc_val, statistic='std', bins=bins)
    return [bin_means, bin_std]


def PeakProfile(kappa, weights, ctx):
    num_bins = ctx['PeakProfile_bins']  # number of bins

    # get peak positions
    peakfinder = importlib.import_module('.stats.Peaks', package='estats')
    peak_pos = peakfinder.Peaks(kappa, weights, ctx)[1]  # [theta,phi] in deg

    # convert to radians and colatitute (drop delimiter)
    theta = np.pi / 2. - deg2rad(peak_pos[:-1, 0])
    phi = deg2rad(peak_pos[:-1, 1])

    # check ranges
    assert np.all((theta >= 0.0) & (theta <= np.pi))
    assert np.all((phi >= 0.0) & (phi <= 2. * np.pi))

    means = np.zeros(num_bins)
    std = np.zeros(num_bins)

    # iterate over peaks
    num_peaks = theta.size
    bins = np.linspace(0.0, 5. / 4. * ctx['scale'], num_bins + 1)
    counts = np.zeros(num_bins, dtype=int)
    for k in range(0, num_peaks):
        binpro = binned_profile(
            kappa, ctx['NSIDE'], ctx['scale'], bins, theta[k], phi[k], ctx)
        counts += np.logical_not(np.isnan(binpro[0]))
        means += np.nan_to_num(binpro[0])
        std += np.nan_to_num(binpro[1])

    means /= counts
    std /= counts

    # estimate std of means
    std /= np.sqrt(counts)

    return [means, std]


def process(data, ctx, scale_to_unity=False):

    data = data[::2, :]

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
    operation = 'average'

    n_bins_sliced = ctx['PeakProfile_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    num_of_scales = len(ctx['scales'])
    n_bins_sliced = ctx['PeakProfile_bins']

    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    for scale in ctx['scales']:
        bin_edges_ = np.linspace(0.0, 5. / 4. * scale,
                                 ctx['PeakProfile_bins'] + 1)
        bin_centers = np.vstack(
            (bin_centers,
             bin_edges_[:-1] + 0.5 * (bin_edges_[1:] - bin_edges_[:-1])))
        bin_edge_indices = np.vstack(
            (bin_edge_indices, np.arange(n_bins_sliced + 1)))

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['PeakProfile_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['PeakProfile_bins']
            f = np.asarray(f)
        filter = np.append(filter, f)
    return filter
