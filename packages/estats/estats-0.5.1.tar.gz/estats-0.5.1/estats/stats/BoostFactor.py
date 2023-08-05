# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Nicole Leemann, adapted by Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['scale', 'NSIDE', 'SNR_bins', 'R_bins',
                'scales', 'selected_scales', 'SNR_min', 'SNR_max']
    defaults = [21.1, 1024, 10, 10,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                    15.8, 13.2, 10.5, 7.9, 5.3, 2.6],
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2, 10.5],
                0.0, 5.0]
    types = ['float', 'int', 'int', 'int', 'list', 'list', 'float', 'float']
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


def BoostFactor(kappa, weights, ctx):
    # standard devaition of map
    sig = np.std(kappa[kappa > hp.pixelfunc.UNSEEN])
    ell = kappa.size

    # Exclude last element
    nside = hp.get_nside(kappa)
    ran = np.arange(ell - 1)

    temp = kappa[-1]
    kappa[-1] = hp.pixelfunc.UNSEEN

    peaks = np.zeros(0, dtype=np.int)

    # calculate all the neighbours, chunked (slow but slim memory)
    num_chunks = 2
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        edges = np.any(kappa[neighbours] == hp.pixelfunc.UNSEEN, axis=0)

        # Get Peak positions (maxima)
        ps = np.all(kappa[neighbours] < kappa[r], axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        ps = np.logical_and(ps, np.logical_not(edges))

        peaks = np.append(peaks, r[ps])

    # Last Value treatment
    kappa[-1] = temp
    n0 = hp.get_all_neighbours(nside, ell - 1)
    if (np.all(kappa[n0] < kappa[ell - 1])):
        peaks = np.append(peaks, ell - 1)
    n1 = np.reshape(hp.get_all_neighbours(nside, n0).T, (-1))
    peaks2 = np.all(np.reshape(kappa[n1], (-1, 8))
                    < kappa[n0].reshape((-1, 1)), axis=1)
    peaks2 = n0[peaks2]
    peaks = _select(n1, peaks, peaks2)

    peak_vals = kappa[peaks]
    peak_theta, peak_phi = hp.pixelfunc.pix2ang(ctx['NSIDE'], peaks)
    peak_SNRs = peak_vals / sig

    SNR_edges = np.linspace(
        ctx['SNR_min'], ctx['SNR_max'], ctx['SNR_bins'] + 1)
    R_bins = np.linspace(0.0, 5. / 4. * ctx['scale'], ctx['R_bins'] + 1)
    radius = arcmin2rad(5. / 4. * ctx['scale'])

    out = np.zeros(0)
    for SNR in range(ctx['SNR_bins']):
        peak_sel = (peak_SNRs >= SNR_edges[SNR]) \
            & (peak_SNRs < SNR_edges[SNR + 1])
        peak_pixels = peaks[peak_sel]
        thetas = peak_theta[peak_sel]
        phis = peak_phi[peak_sel]

        distances = np.zeros(0)
        counts = np.zeros(0)
        for idp, p in enumerate(peak_pixels):
            cen_vec = hp.pixelfunc.pix2vec(nside, p)
            disc_pix = hp.query_disc(nside, cen_vec, radius)
            disc_ang = hp.pixelfunc.pix2ang(nside, disc_pix)
            disc_th = disc_ang[0]
            disc_ph = disc_ang[1]

            dth = disc_th - thetas[idp]
            dph = disc_ph - phis[idp]
            disc_r = np.sqrt(dth ** 2 + dph ** 2)
            disc_r = rad2arcmin(disc_r)  # in arcmin

            distances = np.append(distances, disc_r)
            counts = np.append(counts, weights[disc_pix])

        # bin pixels
        if len(counts) > 0:
            bin_means = np.zeros(0)
            for r in range(len(R_bins) - 1):
                idr = (distances >= R_bins[r]) & (distances < R_bins[r + 1])
                val = np.mean(counts[idr])
                bin_means = np.append(bin_means, val)
        else:
            bin_means = np.full(ctx['R_bins'], np.nan)
        out = np.append(out, bin_means)

    return out


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
    mult = ctx['SNR_bins']
    # number of scales
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'average'

    n_bins_sliced = ctx['R_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # First row of bin_centers indicates the SNR centers
    n_bins_sliced = ctx['R_bins']

    bin_centers = np.zeros((0, ctx['SNR_bins'] * n_bins_sliced))
    bin_edge_indices = np.zeros((0, n_bins_sliced + 1))

    SNR_edges = np.linspace(
        ctx['SNR_min'], ctx['SNR_max'], ctx['SNR_bins'] + 1)
    SNR_centers = SNR_edges[:-1] + 0.5 * (SNR_edges[1:] - SNR_edges[:-1])
    bin_centers = np.vstack(
        (bin_centers, np.repeat(SNR_centers, n_bins_sliced)))

    for scale in ctx['scales']:
        bins = np.linspace(0.0, 5. / 4. * scale, n_bins_sliced + 1)
        bins = bins[:-1] + 0.5 * (bins[1:] - bins[:-1])
        bins = np.tile(bins, ctx['SNR_bins'])
        bin_centers = np.vstack((bin_centers, bins))
        bin_edge_indices = np.vstack(
            (bin_edge_indices, np.arange(n_bins_sliced + 1)))

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['R_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['R_bins']
            f = np.asarray(f)

        f = np.tile(f, ctx['SNR_bins'])
        filter = np.append(filter, f)
    return filter
