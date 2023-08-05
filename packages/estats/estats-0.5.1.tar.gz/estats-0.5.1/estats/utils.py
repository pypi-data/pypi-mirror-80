# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import importlib
import pathlib
import glob
import os

from ekit.logger import vprint


def _calc_alms(shear_map_1, shear_map_2, mode='A', logger=None, verbose=False):
    """
    Calculates spherical harmonics given two shear maps.
    Multiplies by appropriate factor to convert to spin-0
    (E, B modes of convergence) according to spherial Kaiser-Squires map
    mapping routine.

    :param shear_map_1: First component Healpix shear map
    :param shear_map_2: Second component Healpix shear map
    :param mode: If E return E modes only, if B return B modes only,
                 if A return both
    :param logger: Logging instance
    :param verbose: Verbose mode
    :return: spherical harmonics E and B modes for spin-0 convergence field.
    """

    if (len(shear_map_1) == 0) | (len(shear_map_2) == 0):
        if mode == 'A':
            return [], []
        elif mode == 'E':
            return []
        elif mode == 'B':
            return []

    # Spin spherical harmonic decomposition
    NSIDE = hp.npix2nside(len(shear_map_1))
    lmax = 3 * NSIDE - 1

    alm_T, alm_E, alm_B = hp.map2alm(
        [np.zeros_like(shear_map_1), shear_map_1, shear_map_2], lmax=lmax)

    ell = hp.Alm.getlm(lmax)[0]

    # Multiply by the appropriate factor for spin convertion
    fac = np.where(np.logical_and(ell != 1, ell != 0),
                   - np.sqrt(((ell + 1.0) * ell) / ((ell + 2.0)
                                                    * (ell - 1.0))), 0)
    vprint("Calculated E and B mode spherical harmonics from shear maps",
           logger=logger, verbose=verbose)

    if mode == 'A':
        alm_E *= fac
        alm_B *= fac
        return alm_E, alm_B
    elif mode == 'E':
        alm_E *= fac
        return alm_E
    elif mode == 'B':
        alm_B *= fac
        return alm_B


def import_executable(stat, func, verbose=False, logger=None):
    """
    Import plugin
    """
    executable = importlib.import_module(
        '.stats.{}'.format(stat), package='estats')
    executable = getattr(executable, func)

    vprint('Imported Function {} from statistics Plugin {}'.format(
        func, stat), logger=logger, verbose=verbose)
    return executable


def get_plugin_contexts(alloweds, typess, defaultss):
    """
    Gets the contexts for the different statistics plugins
    """

    # get all context parameters from the different statistics plugins
    dir = pathlib.Path(__file__).parent.absolute()
    plugin_paths = glob.glob('{}/stats/*.py'.format(dir))
    plugins = []
    for plugin in plugin_paths:
        if ('__init__' in plugin):
            continue
        else:
            plugins.append(os.path.basename(plugin.split('.py')[0]))

    stat_types = {}

    for plugin in plugins:
        allowed, defaults, types, stat_type \
            = import_executable(plugin, 'context')()
        for ii, a in enumerate(allowed):
            if a in alloweds:
                continue
            else:
                alloweds.append(a)
                typess.append(types[ii])
                defaultss.append(defaults[ii])

        stat_types[plugin] = stat_type
    alloweds.append('stat_types')
    defaultss.append(stat_types)
    types.append('dict')
    return alloweds, typess, defaultss
