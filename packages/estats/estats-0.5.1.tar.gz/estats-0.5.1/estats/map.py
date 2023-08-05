# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import copy
import os

from ekit import context
from estats import utils
from ekit.logger import vprint
from ekit import paths


class map:
    """
    The map module handles shear and convergence maps and calculate summary
    statistics from them.
    One instance can hold up to two sets of weak lensing maps. Each set
    is constituted out of a survey mask, a trimmed survey mask (tighter survey
    mask meant to be used to disregard pixels at the edge of the mask, where
    large errors are introduced due to the spherical harmonics transformation),
    2 convergence maps (E and B modes),
    a weight map and 2 shear maps (first and second component).

    The summary statistics are defined via plugins that are located in the
    estats.stats folder. This allows users to easily add their own summary
    statistic without having to modify the internals of the code.
    See the :ref:`own_stat` Section to learn how to do that.

    The summary statistics can be calculated from the shear maps, the
    convergence maps or from a smoothed convergence maps (multiscale approach
    for extraction of non-Gaussian features).

    If only one set of weak lensing maps is given the statistics will be
    calculated from that set directly. If two sets are given and the name of
    the statistic to be computed contains the word Cross both sets are passed
    to the statistics plugin. This can be used to calculate cross-correlations
    between maps from different tomographic bins for example.

    The most important functionalities are:

    - convert_convergence_to_shear:

        Uses spherical Kaiser-Squires to convert the internal shear maps to
        convergence maps. The maps are masked using the internal masks.
        By default the trimmed mask is used to allow the user to disregard
        pixels where the spherical harmonics transformation introduced large
        errors.

    - convert_shear_to_convergence:

        Uses spherical Kaiser-Squires to convert the internal E-mode
        convergence map to shear maps. The maps are masked using the internal
        masks. By default the trimmed mask is used to allow the user to
        disregard pixels where the spherical harmonics transformation
        introduced large errors.

    - smooth_maps:

        Applies a Gaussian smoothing kernel to all internal convergence maps
        (E- and B-modes). The fwhm parameter decides on the FWHM of the
        Gaussian smoothing kernel. It is given in arcmin.

    - calc_summary_stats:

        Main functionality of the module. Allows to use statistics plugins
        located in the estats.stats folder to calculate map based statistics.

        See the :ref:`own_stat` Section to learn how the statistics plugins
        look like and how to make your own one.

        The summary statistics can be calculated from the shear maps, the
        convergence maps or from a smoothed convergence maps (multiscale
        approach for extraction of non-Gaussian features).

        If only one set of weak lensing maps is given the statistics will be
        calculated from that set directly. If two sets are given and the name
        of the statistic to be computed contains the word Cross both sets are
        passed to the statistics plugin. This can be used to calculate
        cross-correlations
        between maps from different tomographic bins for example.

        Instead of using the internal masks for masking, extra masks can be
        used. This allows to use maps with multiple survey cutouts on it and
        select a different cutout each time the function is called.

        If use_shear_maps is set to True the function will convert the shear
        maps into convergence maps using spherical Kaiser-Squires instead of
        using the convergence maps directly.

        If copy_obj is set to False, no copies of the internal maps are made.
        This can save RAM but it also leads to the internal maps being
        overwritten. If you wish to use the internal maps after the function
        call set this to True!

        By default the function returns the calculated statistics in a
        dictionary. But if write_to_file is set to True it will append to
        files that are defined using the defined_parameters,
        undefined_parameters, output_dir and name arguments using ekit.paths.

        Note: If the CrossCLs statistic is used without secondary maps set the
        convergence and weights maps will be written onto a Healpix map.
        The path to the map is defined over the defined_parameters,
        undefined_parameters, output_dir and name arguments using ekit.paths.

    The accepted keywords are:

    - NSIDE:

        default: 1024

        choices: an integer being a power of 2

        The Healpix resolution that is used to produce the map products.

    - scales:

        default:
        [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2, 10.5, 7.9, 5.3, 2.6]

        choices:  A list of floats indicating the FWHM of the Gaussian
        smoothing kernels to be applied in arcmin.

        For summary statistics that are of the multi type (see :ref:`own_stat`)
        the summary statistics are extracted from the convergence maps for
        a number of scales (multiscale approach). To do so the maps are
        smoothed with Gaussian smoothing kernels of different size.
        The scales indicate the FWHM of these scales.

    - polarizations:

        default: 'A'

        choices: 'E', 'B', 'A'

        If E only returns E-mode statistics only when calc_summary_stats is
        used.
        If B only returns B-mode statistics only when calc_summary_stats is
        used.
        If A both E- and B-mode statistics are returned when calc_summary_stats
        is used.

    - prec:

        default: 32

        choices: 64, 32, 16

        Size of the float values in the Healpix maps in bits. For less then 32
        hp.UNSEEN is mapped to -inf -> No RAM optimization anymore
    """

    def __init__(self, gamma_1=[], gamma_2=[], kappa_E=[], kappa_B=[],
                 mask=[], trimmed_mask=[], weights=[],
                 gamma_1_sec=[], gamma_2_sec=[], kappa_E_sec=[],
                 kappa_B_sec=[],
                 mask_sec=[], trimmed_mask_sec=[], weights_sec=[],
                 context_in={}, logger=None, verbose=False, **kwargs):
        """
        Initialization function for the map class.

        :param gamma_1: Map for first shear component
        :param gamma_2: Map for second shear component
        :param gamma_1_sec: Second set of maps. Map for first shear component
        :param gamma_2_sec: Second set of maps. Map for second shear component
        :param kappa_E: Map for convergence E-modes
        :param kappa_B: Map for convergence B-modes
        :param mask: Optionally can provide a mask that is applied to the maps.
        :param mask_sec: Mask for second map.
        :param trimmed_mask: Optionally can provide a stricter mask that is
                             applied to the convergence maps if they are
                             generated from the shear maps.
        :param trimmed_mask_sec: Trimmed Mask for second map.
        :param weights: Can provide a map conatining the pixel weights.
        :param weights_sec: Second set of weights.
        :param context_in: A dictionary containing parameters used by class.
        :param logger: A logger instance.
        :param verbose: Triggers verbose mode. Persistent for the whole class.
        """

        self.verbose = verbose
        self.logger = logger

        # setup context
        allowed = ['NSIDE', 'scales', 'polarizations', 'prec']

        types = ['int', 'list', 'str', 'int']

        defaults = [1024, [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                           10.5, 7.9, 5.3, 2.6], 'A', 32]

        allowed, types, defaults = utils.get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            logger=self.logger, verbose=self.verbose)

        self.ctx['prec'] = 'float{}'.format(self.ctx['prec'])

        self.set_mask(mask, sec=False, apply=False)
        self.set_mask(mask_sec, sec=True, apply=False)

        self.set_trimmed_mask(trimmed_mask, sec=False, apply=False)
        self.set_trimmed_mask(trimmed_mask_sec, sec=True, apply=False)

        self.set_weights(weights=weights, sec=False)
        self.set_weights(weights=weights_sec, sec=True)

        self.set_shear_maps(gamma_1, gamma_2, sec=False)
        self.set_shear_maps(gamma_1_sec, gamma_2_sec, sec=True)

        self.set_convergence_maps(kappa_E, kappa_B, sec=False)
        self.set_convergence_maps(kappa_E_sec, kappa_B_sec, sec=True)

    # ACCESING OBJECTS

    def get_shear_maps(self, trimming=False, sec=False):
        """
        Returns the shear maps

        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        :param sec: If True sets secondary objects
        """
        if sec:
            if (len(self.gamma_1_sec) == 0) | (len(self.gamma_2_sec) == 0):
                vprint("Secondary shear maps not set. Calculating from "
                       "convergence maps.", logger=self.logger, verbose=True,
                       level='warning')
                gamma_1, gamma_2 = self._convert_kappa_to_gamma(
                    sec=True, trimming=trimming)
            else:
                gamma_1 = self.gamma_1_sec
                gamma_2 = self.gamma_2_sec
        else:
            if (len(self.gamma_1) == 0) | (len(self.gamma_2) == 0):
                vprint("Primary shear maps not set. Calculating from "
                       "convergence maps.", logger=self.logger, verbose=True,
                       level='warning')
                gamma_1, gamma_2 = self._convert_kappa_to_gamma(
                    sec=False, trimming=trimming)
            else:
                gamma_1 = self.gamma_1
                gamma_2 = self.gamma_2
        return (gamma_1, gamma_2)

    def get_weights(self, sec=False):
        """
        Returns the weight maps

        :param sec: If True sets secondary objects
        """
        if sec:
            return self.weights_sec
        else:
            return self.weights

    def get_mask(self, sec=False):
        """
        Returns the mask

        :param sec: If True sets secondary objects
        """
        if sec:
            return self.mask_sec
        else:
            return self.mask

    def get_trimmed_mask(self, sec=False):
        """
        Returns the trimmed mask

        :param sec: If True sets secondary objects
        """
        if sec:
            return self.trimmed_mask_sec
        else:
            return self.trimmed_mask

    def get_convergence_maps(self, trimming=False, sec=False):
        """
        Returns the convergence maps (E and B mode maps)

        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        :param sec: If True sets secondary objects
        """
        if sec:
            if (len(self.kappa_E_sec) == 0) | (len(self.kappa_B_sec) == 0):
                vprint("Secondary converge maps not set. Calculating from "
                       "shear maps.", logger=self.logger, verbose=True,
                       level='warning')
                kappa_E_sec, kappa_B_sec = self._convert_gamma_to_kappa(
                    sec=True, trimming=trimming)
            else:
                kappa_E = self.kappa_E_sec
                kappa_B = self.kappa_B_sec
        else:
            if (len(self.kappa_E) == 0) | (len(self.kappa_B) == 0):
                vprint("Primary convergence maps not set. Calculating from "
                       "shear maps.", logger=self.logger, verbose=True,
                       level='warning')
                kappa_E, kappa_B = self._convert_gamma_to_kappa(
                    sec=False, trimming=trimming)
            else:
                kappa_E = self.kappa_E
                kappa_B = self.kappa_B
        return (kappa_E, kappa_B)

    # CLEARING OBJECTS

    def clear_shear_maps(self):
        """
        Clears the shear maps
        """
        self.gamma_1 = []
        self.gamma_2 = []
        self.gamma_1_sec = []
        self.gamma_2_sec = []
        vprint("Cleared shear maps", logger=self.logger, verbose=self.verbose)

    def clear_convergence_maps(self):
        """
        Clears the convergence maps
        """
        self.kappa_E = []
        self.kappa_B = []
        self.kappa_E_sec = []
        self.kappa_B_sec = []
        vprint("Cleared convergence maps",
               logger=self.logger, verbose=self.verbose)

    def clear_weights(self):
        """
        Clears the weight maps
        """
        self.weights = []
        self.weights_sec = []
        vprint("Cleared weights", logger=self.logger, verbose=self.verbose)

    def clear_mask(self):
        """
        Clears the mask
        """
        self.mask = []
        self.mask_sec = []
        vprint("Cleared mask", logger=self.logger, verbose=self.verbose)

    def clear_trimmed_mask(self):
        """
        Clears the trimmed mask
        """
        self.trimmed_mask = []
        self.trimmed_mask_sec = []
        vprint("Cleared trimmed_mask", logger=self.logger,
               verbose=self.verbose)

    # SETTING OBJECTS

    def set_shear_maps(self, shear_1=[], shear_2=[], sec=False):
        """
        Sets the shear maps

        :param shear_1: First shear map component
        :param shear_2: Second shear map component
        :param sec: If True sets secondary objects
        """
        shear_1 = np.asarray(shear_1, dtype=self.ctx['prec'])
        shear_2 = np.asarray(shear_2, dtype=self.ctx['prec'])

        if sec:
            self.gamma_1_sec = self._apply_mask(
                shear_1, sec=True, obj_name='secondary shear 1')
            self.gamma_2_sec = self._apply_mask(
                shear_2, sec=True, obj_name='secondary shear 2')
            vprint("Set secondary shear maps",
                   logger=self.logger, verbose=self.verbose)
        else:
            self.gamma_1 = self._apply_mask(shear_1, obj_name='shear 1')
            self.gamma_2 = self._apply_mask(shear_2, obj_name='shear 2')
            vprint("Set primary shear maps",
                   logger=self.logger, verbose=self.verbose)

    def set_convergence_maps(self, kappa_E=[], kappa_B=[], sec=False):
        """
        Sets the convergence E and B maps

        :param kappa_E: E mode convergence map
        :param kappa_B: B mode convergence map
        :param sec: If True sets secondary objects
        """
        kappa_E = np.asarray(kappa_E, dtype=self.ctx['prec'])
        kappa_B = np.asarray(kappa_B, dtype=self.ctx['prec'])

        if sec:
            self.kappa_E_sec = self._apply_mask(
                kappa_E, sec=True, obj_name='secondary convergence E-modes')
            self.kappa_B_sec = self._apply_mask(
                kappa_B, sec=True, obj_name='secondary convergence B-modes')
            vprint("Set secondary convergence maps",
                   logger=self.logger, verbose=self.verbose)
        else:
            self.kappa_E = self._apply_mask(
                kappa_E, obj_name='convergence E-modes')
            self.kappa_B = self._apply_mask(
                kappa_B, obj_name='convergence B-modes')
            vprint("Set primary convergence maps",
                   logger=self.logger, verbose=self.verbose)

    def set_weights(self, weights=[], sec=False):
        """
        Sets the weight map

        :param weights: The weight map
        :param sec: If True sets secondary objects
        """
        weights = np.asarray(weights, dtype=self.ctx['prec'])

        if sec:
            self.weights_sec = self._apply_mask(weights, sec=True,
                                                obj_name='secondary weights')
            vprint("Set secondary weights",
                   logger=self.logger, verbose=self.verbose)
        else:
            self.weights = self._apply_mask(weights, obj_name='weights')
            vprint("Set primary weights",
                   logger=self.logger, verbose=self.verbose)

    def set_mask(self, mask=[], sec=False, apply=True):
        """
        Sets the mask

        :param mask: The mask to set
        :param sec: If True sets secondary objects
        :param apply: If True directly applies the set mask to the weights,
                      convergence maps and shear maps
        """
        mask = np.asarray(mask, dtype=bool)

        if sec:
            self.mask_sec = mask
            vprint("Set secondary convergence mask",
                   logger=self.logger, verbose=self.verbose)
            if apply:
                self.weights_sec = self._apply_mask(
                    self.weights_sec, sec=True, obj_name='secondary weights')
                self.gamma_1_sec = self._apply_mask(
                    self.gamma_1_sec, sec=True, obj_name='secondary shear 1')
                self.gamma_2_sec = self._apply_mask(
                    self.gamma_2_sec, sec=True, obj_name='secondary shear 2')
                self.kappa_E_sec = self._apply_mask(
                    self.kappa_E_sec, sec=True,
                    obj_name='secondary convergence E')
                self.kappa_B_sec = self._apply_mask(
                    self.kappa_B_sec, sec=True,
                    obj_name='secondary convergence B')
        else:
            self.mask = mask
            vprint("Set primary convergence mask",
                   logger=self.logger, verbose=self.verbose)
            if apply:
                self.weights = self._apply_mask(
                    self.weights, obj_name='weights')
                self.gamma_1 = self._apply_mask(
                    self.gamma_1, obj_name='shear 1')
                self.gamma_2 = self._apply_mask(
                    self.gamma_2, obj_name='shear 2')
                self.kappa_E = self._apply_mask(
                    self.kappa_E, obj_name='convergence E')
                self.kappa_B = self._apply_mask(
                    self.kappa_B, obj_name='convergence B')

    def set_trimmed_mask(self, trimmed_mask=[], sec=False, apply=False):
        """
        Sets the trimmed mask

        :param trimmed_mask: The trimmed mask to set
        :param sec: If True sets secondary objects
        :param apply: If True directly applies the set mask to the weights,
                      convergence maps and shear maps
        """
        trimmed_mask = np.asarray(trimmed_mask, dtype=bool)

        if sec:
            self.trimmed_mask_sec = trimmed_mask
            vprint("Set secondary trimmed mask",
                   logger=self.logger, verbose=self.verbose)
            if apply:
                self.weights_sec = self._apply_mask(
                    self.weights_sec, trimming=True, sec=True,
                    obj_name='secondary weights')
                self.gamma_1_sec = self._apply_mask(
                    self.gamma_1_sec, trimming=True, sec=True,
                    obj_name='secondary shear 1')
                self.gamma_2_sec = self._apply_mask(
                    self.gamma_2_sec, trimming=True, sec=True,
                    obj_name='secondary shear 2')
                self.kappa_E_sec = self._apply_mask(
                    self.kappa_E_sec, trimming=True, sec=True,
                    obj_name='secondary convergence E')
                self.kappa_B_sec = self._apply_mask(
                    self.kappa_B_sec, trimming=True, sec=True,
                    obj_name='secondary convergence B')
        else:
            self.trimmed_mask = trimmed_mask
            vprint("Set primary trimmed mask",
                   logger=self.logger, verbose=self.verbose)
            if apply:
                self.weights = self._apply_mask(
                    self.weights, trimming=True, obj_name='weights')
                self.gamma_1 = self._apply_mask(
                    self.gamma_1, trimming=True, obj_name='shear 1')
                self.gamma_2 = self._apply_mask(
                    self.gamma_2, trimming=True, obj_name='shear 2')
                self.kappa_E = self._apply_mask(
                    self.kappa_E, trimming=True, obj_name='convergence E')
                self.kappa_B = self._apply_mask(
                    self.kappa_B, trimming=True, obj_name='convergence B')

    # METHODS

    def convert_shear_to_convergence(self, sec=False, trimming=True):
        """
        Calculates convergence maps from the shear maps and sets them
        (retrieve with get_convergence_maps).

        :param sec: If True sets secondary objects
        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        """
        kappa_E, kappa_B = self._convert_gamma_to_kappa(
            sec=sec, trimming=trimming)
        if sec:
            self.kappa_E_sec = kappa_E
            self.kappa_B_sec = kappa_B
        else:
            self.kappa_E = kappa_E
            self.kappa_B = kappa_B

    def convert_convergence_to_shear(self, sec=False, trimming=True):
        """
        Calculates shear maps from the convergence maps and sets them
        (retrieve with get_shear_maps).

        :param sec: If True sets secondary objects
        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        """
        gamma_1, gamma_2 = self._convert_kappa_to_gamma(
            sec=sec, trimming=trimming)

        if sec:
            self.gamma_1_sec = gamma_1
            self.gamma_2_sec = gamma_2
        else:
            self.gamma_1 = gamma_1
            self.gamma_2 = gamma_2

    def smooth_maps(self, fwhm=0.0, sec=False):
        """
        Smooth the kappa maps with a Gaussian kernel

        :param fwhm: The FWHM of the smoothing kernel in arcmins
        :param sec: If True sets secondary objects
        """

        if sec:
            kappa_E = self.kappa_E_sec
            kappa_B = self.kappa_B_sec
        else:
            kappa_E = self.kappa_E
            kappa_B = self.kappa_B

        if len(kappa_E) > 0:
            if fwhm > 0.0:
                kappa_E = np.asarray(
                    hp.sphtfunc.smoothing(
                        kappa_E,
                        fwhm=np.radians(float(fwhm) / 60.)),
                    dtype=self.ctx['prec'])
            kappa_E = self._apply_mask(
                kappa_E, sec=sec, obj_name='convegence E-modes')
        if len(kappa_B) > 0:
            if fwhm > 0.0:
                kappa_B = np.asarray(
                    hp.sphtfunc.smoothing(
                        kappa_B,
                        fwhm=np.radians(float(fwhm) / 60.)),
                    dtype=self.ctx['prec'])
            kappa_B = self._apply_mask(
                kappa_B, sec=sec, obj_name='convegence B-modes')

        if sec:
            self.kappa_E_sec = kappa_E
            self.kappa_B_sec = kappa_B
            vprint("Smoothed secondary convergence maps with a Gaussian "
                   "smoothing kernel of FWHM {} arcmin".format(
                       fwhm), logger=self.logger, verbose=self.verbose)
        else:
            self.kappa_E = kappa_E
            self.kappa_B = kappa_B
            vprint("Smoothed primary convergence maps with a Gaussian "
                   "smoothing kernel of FWHM {} arcmin".format(
                       fwhm), logger=self.logger, verbose=self.verbose)

    def calc_summary_stats(self, statistics, mask=[], mask_sec=[],
                           trimmed_mask=[], trimmed_mask_sec=[], scales=[],
                           use_shear_maps=False, output_dir='.',
                           defined_parameters={}, undefined_parameters=[],
                           name='', copy_obj=True, write_to_file=False):
        """
        Calculates the summary statistics from the maps
        Can provide a mask or trimmed_mask which will be used instead of the
        internal masks, allowing to store multiple cutouts on a single mask
        (can save memory)

        :param statistics: Statistcs to calculate.
        :param mask: Can provide an additional mask, otherwise internal mask
                     used
        :param mask_sec: Mask for second map
        :param trimmed_mask: Can provide an additional trimmed mask
        :param trimmed_mask_sec: Second trimmed mask
        :param scales: Smoothing scales to apply for multiscale analysis for
                       Non-Gaussian statistics (multi type) (FWHM in arcmins).
                       If not given uses internal scales from context
        :param use_shear_maps: If set to True will calculate convergence maps
                               from shear maps for convergence map based
                               statistics. Otherwise uses
                               the convergence maps directly.
        :param output_dir: If write_to_file is True used to build the output
                           path. See ekit docs.
        :param defined_parameters: If write_to_file is True used to build the
                                   output path. See ekit docs
        :param undefined_parameters: If write_to_file is True used to build
                                     the output path. See ekit docs
        :param name: If write_to_file is True used to build the output
                     path. See ekit docs
        :param copy_obj: If True preserves the map objects, otherwise
                         overwrites them with masked maps in the extraction
                         process
        :param write_to_file: If True appends to files directly instead of
                              returning the results as a dictionary
        """

        if not copy_obj:
            vprint(
                "Using internal map objects directly and potentially "
                "overwriting them! Do not use this mode if you wish to "
                "further use the map objects of this class instance. "
                "Also make sure that your statistic plugins do not overwrite "
                "maps.",
                logger=self.logger, verbose=True, level='warning')

        if len(scales) == 0:
            scales = self.ctx['scales']

        stats = self._get_pol_stats(statistics)

        # import statistics plugins
        plugins = {}
        for statistic in stats['E']:
            if statistic == '2PCF':
                statistic = 'Peaks'
            elif statistic == '2VCF':
                statistic = 'Voids'
            plugins[statistic] = utils.import_executable(statistic,
                                                         statistic,
                                                         self.verbose,
                                                         self.logger)

        # set polarizations
        polarizations = []
        if (self.ctx['polarizations'] == 'A') | \
           (self.ctx['polarizations'] == 'E'):
            polarizations.append('E')
        if (self.ctx['polarizations'] == 'A') | \
           (self.ctx['polarizations'] == 'B'):
            polarizations.append('B')

        # divide statistics into classes
        statistic_divided = self._divide_statistics(stats)

        # collector array for outputs
        outs = {}

        ##################
        # shear statistics
        ##################
        if len(statistic_divided['E']['shear']) > 0:
            outs = self._calc_shear_stats(statistic_divided['E']['shear'],
                                          plugins, outs, polarizations,
                                          mask, mask_sec,
                                          trimmed_mask, trimmed_mask_sec,
                                          copy_obj, write_to_file, name,
                                          output_dir, defined_parameters,
                                          undefined_parameters)
        for pol in polarizations:
            alm, alm_sec, weights, weights_sec = self._prep_alms(
                pol, mask, mask_sec, trimmed_mask, trimmed_mask_sec,
                copy_obj, use_shear_maps)

            ########################
            # convergence statistics
            ########################
            if (len(statistic_divided[pol]['convergence']) > 0):
                outs = self._calc_convergence_stats(
                    outs, plugins, alm,
                    alm_sec, weights, weights_sec,
                    trimmed_mask, trimmed_mask_sec,
                    defined_parameters,
                    undefined_parameters, output_dir,
                    statistic_divided[pol]['convergence'],
                    pol, write_to_file, name, copy_obj)

            ###################################
            # multiscale convergence statistics
            ###################################
            if len(statistic_divided[pol]['multi']) > 0:
                if len(statistic_divided[pol]['multi']) > 0:
                    outs = self._calc_multi_stats(
                        outs, scales, plugins, alm,
                        alm_sec, weights, weights_sec,
                        trimmed_mask, trimmed_mask_sec,
                        defined_parameters,
                        undefined_parameters, output_dir,
                        statistic_divided[pol]['multi'],
                        pol, write_to_file, name, copy_obj, statistics)
        return outs

    ##################################
    # HELPER FUNCTIONS
    ##################################

    def _stack_stats(self, stat_out, pol, statistic, all_statistics, outs,
                     store_to_files=False, name='', output_dir='',
                     defined_parameters={}, undefined_parameters=[]):
        """
        Stack the extracted summary statistics for the output
        """
        # Init Polariazation dict if non existent
        if pol not in outs.keys():
            outs[pol] = {}

        if statistic == 'Extremes':
            if ('Peaks' in all_statistics) | ('2PCF' in all_statistics):
                out = stat_out[0:2]
                stat = 'Peaks'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if ('Voids' in all_statistics) | ('2VCF' in all_statistics):
                out = stat_out[2:4]
                stat = 'Voids'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        elif (statistic == 'Peaks') & (len(stat_out) == 2):
            if 'Peaks' in all_statistics:
                out = stat_out[0]
                stat = 'Peaks'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if '2PCF' in all_statistics:
                out = stat_out[1]
                stat = '2PCF'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        elif (statistic == 'Voids') & (len(stat_out) == 2):
            if 'Voids' in all_statistics:
                out = stat_out[0]
                stat = 'Voids'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if '2PCF' in all_statistics:
                out = stat_out[1]
                stat = '2VCF'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        else:
            if store_to_files:
                # adding a separation value
                if (statistic == '2PCF') | (statistic == '2PCF'):
                    stat_out = np.vstack(([[-999.0, -999.0]], stat_out))
                # saving
                output_path = paths.create_path(
                    name,
                    output_dir, {
                        **defined_parameters,
                        **{'mode': pol,
                           'stat': statistic}},
                    undefined_parameters,
                    suffix='.npy')
                if os.path.exists(output_path):
                    out_file = np.load(output_path)
                    out_file = np.vstack(
                        (out_file, stat_out))
                else:
                    out_file = stat_out
                np.save(output_path, out_file)
            else:
                # Init Statistics dict if non existent
                if statistic not in outs[pol].keys():
                    outs[pol][statistic] = stat_out
                else:
                    # adding a separation value
                    if (statistic == '2PCF') | (statistic == '2PCF'):
                        stat_out = np.vstack(([[-999.0, -999.0]], stat_out))

                    outs[pol][statistic] = np.vstack(
                        (outs[pol][statistic], stat_out))
        return outs

    def _convert_alm_to_kappa(self, alm, fwhm):
        """
        Converts spherical harmonics to E and B modes Convergence maps.
        Can also apply smoothing.
        """
        # smoothing alms with gaussian kernel
        if fwhm > 0.0:
            alm_ = hp.sphtfunc.smoothalm(
                alm, fwhm=np.radians(float(fwhm) / 60.), inplace=False)
        else:
            alm_ = copy.copy(alm)
        kappa = np.asarray(hp.alm2map(alm_, nside=self.ctx['NSIDE']),
                           dtype=self.ctx['prec'])
        return kappa

    def _convert_gamma_to_kappa(self, sec=False, trimming=False):
        """
        Converts two shear maps to convergence maps (E and B modes).
        """
        sign_flip = True

        if sec:
            gamma_1 = self.gamma_1_sec
            gamma_2 = self.gamma_2_sec
        else:
            gamma_1 = self.gamma_1
            gamma_2 = self.gamma_2

        if (len(gamma_1) == 0) | (len(gamma_2) == 0):
            if sec:
                vprint("Secondary shear maps not set -> "
                       "Cannot transform to convergence maps",
                       logger=self.logger, verbose=self.verbose,
                       level='warning')
            else:
                vprint("Primary shear maps not set -> "
                       "Cannot transform to convergence maps",
                       logger=self.logger, verbose=self.verbose,
                       level='warning')
            return [], []

        # spherical harmonics decomposition
        if sign_flip & (len(gamma_1) > 0):
            vprint("Applying sign flip", logger=self.logger,
                   verbose=self.verbose)
            gamma_1[gamma_1 > hp.UNSEEN] *= -1.
        alm_E, alm_B = utils._calc_alms(
            gamma_1, gamma_2)
        if sign_flip & (len(gamma_1) > 0):
            gamma_1[gamma_1 > hp.UNSEEN] *= -1.

        kappa_E = np.asarray(self._convert_alm_to_kappa(alm_E, fwhm=0.0),
                             dtype=self.ctx['prec'])
        kappa_B = np.asarray(self._convert_alm_to_kappa(alm_B, fwhm=0.0),
                             dtype=self.ctx['prec'])

        kappa_E = self._apply_mask(
            kappa_E, sec=sec, trimming=trimming,
            obj_name='convergence E-modes')
        kappa_B = self._apply_mask(
            kappa_B, sec=sec, trimming=trimming,
            obj_name='convergence B-modes')

        return kappa_E, kappa_B

    def _convert_kappa_to_gamma(self, sec=False, trimming=False):
        """
        Converts a kappa map to two shear maps using Kaiser-Squires
        """

        sign_flip = True

        # Maximum l limited by the map resolution
        lmax = 3 * self.ctx['NSIDE'] - 1

        if sec:
            kappa = self.kappa_E_sec
        else:
            kappa = self.kappa_E

        if len(kappa) == 0:
            if sec:
                vprint("Secondary E-mode convergence map not set -> "
                       "Cannot transform to shear maps",
                       logger=self.logger, verbose=self.verbose,
                       level='warning')
            else:
                vprint("Primary E-mode convergence map not set -> "
                       "Cannot transform to shear maps",
                       logger=self.logger, verbose=self.verbose,
                       level='warning')
            return [], []

        # spherical harmonics decomposition
        kappa_alm = hp.map2alm(kappa, lmax=lmax)
        ell = hp.Alm.getlm(lmax)[0]

        # Add the apropriate factor to the kappa_alm
        check = np.logical_and(ell != 1, ell != 0)

        fac = np.where(
            check, -np.sqrt(((ell + 2.0) * (ell - 1)) / ((ell + 1) * ell)), 0)
        kappa_alm *= fac

        # Spin spherical harmonics
        # Q and U are the real and imaginary parts of the shear map
        T, Q, U = hp.alm2map([np.zeros_like(kappa_alm), kappa_alm,
                              np.zeros_like(kappa_alm)],
                             nside=self.ctx['NSIDE'])
        Q = np.asarray(Q, dtype=self.ctx['prec'])
        U = np.asarray(U, dtype=self.ctx['prec'])

        # - sign accounts for the Healpix sign flip
        if sign_flip:
            Q = -1. * Q

        gamma_1 = self._apply_mask(
            Q, trimming=trimming, sec=sec, obj_name='shear 1')
        gamma_2 = self._apply_mask(
            U, trimming=trimming, sec=sec, obj_name='shear 2')

        if sec:
            vprint("Converted secondary E-mode convergence map to shear maps",
                   logger=self.logger, verbose=self.verbose)
        else:
            vprint("Converted primary E-mode convergence map to shear maps",
                   logger=self.logger, verbose=self.verbose)
        return (gamma_1, gamma_2)

    def _apply_mask(self, obj, sec=False, trimming=False, mask=[],
                    obj_name=''):
        """
        Apply masks to maps
        """

        if 'secondary' in obj_name:
            verb = self.verbose
        else:
            verb = True

        if len(obj) == 0:
            vprint("Cannot apply mask to {} map since "
                   "{} object not set. Ignoring...".format(obj_name, obj_name),
                   logger=self.logger, verbose=verb, level='warning')
            return obj

        # use given mask or internals
        if len(mask) == 0:
            if sec:
                if trimming:
                    mask = self.trimmed_mask_sec
                else:
                    mask = self.mask_sec
            else:
                if trimming:
                    mask = self.trimmed_mask
                else:
                    mask = self.mask

        if len(mask) > 0:
            if len(mask) != len(obj):
                raise Exception(
                    "The mask and the object {} that you are trying to mask "
                    "do not have the same size!".format(obj_name))
            mask = np.logical_not(mask)
            if 'weight' in obj_name:
                obj[mask] = 0.0
            else:
                obj[mask] = hp.pixelfunc.UNSEEN
            vprint("Applied mask to object {}".format(obj_name),
                   logger=self.logger, verbose=self.verbose)
        else:
            vprint(
                "No mask found to apply to {} map. Ignoring...".format(
                    obj_name),
                logger=self.logger, verbose=verb, level='warning')
        return obj

    def _calc_shear_stats(self, statistics, plugins, outs, pols,
                          mask=[], mask_sec=[],
                          trimmed_mask=[], trimmed_mask_sec=[],
                          copy_obj=True, write_to_file=False, name='',
                          output_dir='', defined_parameters={},
                          undefined_parameters=[]):

        g_1, g_2, g_1_sec, g_2_sec, weights, weights_sec = \
            self._prep_shear_maps(mask, mask_sec, copy_obj)

        for stat in statistics:
            if 'Cross' in stat:
                stat_out = plugins[stat](
                    copy.copy(g_1), copy.copy(g_2),
                    copy.copy(g_1_sec), copy.copy(g_2_sec),
                    copy.copy(weights), copy.copy(weights_sec), self.ctx)
            else:
                stat_out = plugins[stat](copy.copy(g_1), copy.copy(g_2),
                                         copy.copy(weights), self.ctx)
            if 'E' in pols:
                outs = self._stack_stats(
                    stat_out[0], 'E', stat, [], outs,
                    write_to_file, name, output_dir,
                    defined_parameters, undefined_parameters)
            if 'B' in pols:
                outs = self._stack_stats(
                    stat_out[1], 'B', stat, [], outs,
                    write_to_file, name, output_dir,
                    defined_parameters, undefined_parameters)
        return outs

    def _get_pol_stats(self, statistics):
        stats_ = copy.copy(statistics)
        stats = {}
        stats['E'] = copy.copy(stats_)
        stats['B'] = copy.copy(stats_)
        return stats

    def _calc_convergence_stats(self, outs, plugins, alm,
                                alm_sec, weights, weights_sec,
                                trimmed_mask, trimmed_mask_sec,
                                defined_parameters,
                                undefined_parameters, output_dir,
                                stats, pol,
                                write_to_file, name, copy_obj):
        if len(alm) > 0:
            kappa = self._convert_alm_to_kappa(alm, 0.0)
            vprint("Converted shear maps to convergence maps",
                   logger=self.logger, verbose=self.verbose)
        else:
            if (pol == 'E') & (len(self.kappa_E) == 0):
                self.convert_shear_to_convergence()
            if (pol == 'B') & (len(self.kappa_B) == 0):
                self.convert_shear_to_convergence()
            if copy_obj:
                if pol == 'E':
                    kappa = copy.copy(self.kappa_E)
                elif pol == 'B':
                    kappa = copy.copy(self.kappa_B)
            else:
                if pol == 'E':
                    kappa = self.kappa_E
                elif pol == 'B':
                    kappa = self.kappa_B

        if len(alm_sec) > 0:
            kappa_sec = self._convert_alm_to_kappa(alm_sec, 0.0)
            vprint("Converted shear maps to convergence maps",
                   logger=self.logger, verbose=self.verbose)
        else:
            if (pol == 'E') & (len(self.kappa_E_sec) == 0):
                self.convert_shear_to_convergence(sec=True)
            if (pol == 'B') & (len(self.kappa_B_sec) == 0):
                self.convert_shear_to_convergence(sec=True)
            if copy_obj:
                if pol == 'E':
                    kappa_sec = copy.copy(self.kappa_E_sec)
                elif pol == 'B':
                    kappa_sec = copy.copy(self.kappa_B_sec)
            else:
                if pol == 'E':
                    kappa_sec = self.kappa_E_sec
                elif pol == 'B':
                    kappa_sec = self.kappa_B_sec

        kappa = self._apply_mask(
            kappa, mask=trimmed_mask, trimming=True,
            obj_name='convergence {}-modes'.format(pol))
        kappa_sec = self._apply_mask(
            kappa_sec, sec=True, mask=trimmed_mask_sec, trimming=True,
            obj_name='secondary convergence {}-modes'.format(pol))

        for stat in stats:
            if 'Cross' in stat:
                if len(kappa_sec) > 0:
                    stat_out = plugins[stat](
                        copy.copy(kappa), copy.copy(kappa_sec),
                        copy.copy(weights), copy.copy(weights_sec), self.ctx)
                    outs = self._stack_stats(
                        stat_out, pol, stat, [], outs,
                        write_to_file, name, output_dir,
                        defined_parameters, undefined_parameters)
                else:
                    path = paths.create_path(
                        'KAPPA',
                        output_dir, {
                            **defined_parameters,
                            **{'mode': pol}},
                        undefined_parameters,
                        suffix='.npy')
                    if os.path.isfile(path):
                        m = np.load(path)
                        m[kappa > hp.UNSEEN] = kappa[kappa > hp.UNSEEN]
                        np.save(path, m)
                    else:
                        np.save(path, kappa)

                    path_w = paths.create_path(
                        'WEIGHTS',
                        output_dir, defined_parameters,
                        undefined_parameters,
                        suffix='.npy')
                    if os.path.isfile(path_w):
                        m = np.load(path_w)
                        m[weights > 0.0] = weights[weights > 0.0]
                        np.save(path_w, m)
                    else:
                        np.save(path_w, weights)
                    vprint(
                        "Second convergence map not given but Cross "
                        "statistic found. Stacked the convergence map "
                        "to file {} and the weights to {}".format(
                            path, path_w), logger=self.logger,
                        verbose=True, level='warning')
            else:
                stat_out = plugins[stat](copy.copy(kappa),
                                         copy.copy(weights), self.ctx)
                outs = self._stack_stats(
                    stat_out, pol, stat, [], outs,
                    write_to_file, name, output_dir,
                    defined_parameters, undefined_parameters)
        return outs

    def _prep_shear_maps(self, mask, mask_sec, copy_obj=True):
        """
        Prepare the masks for statistics extraction
        """
        if len(self.gamma_1) == 0:
            self.convert_convergence_to_shear()
        if len(self.gamma_1_sec) == 0:
            self.convert_convergence_to_shear(sec=True)

        if copy_obj:
            g_1 = copy.copy(self.gamma_1)
            g_2 = copy.copy(self.gamma_2)
            g_1_sec = copy.copy(self.gamma_1_sec)
            g_2_sec = copy.copy(self.gamma_2_sec)
            weights = copy.copy(self.weights)
            weights_sec = copy.copy(self.weights_sec)
        else:
            g_1 = self.gamma_1
            g_2 = self.gamma_2
            g_1_sec = self.gamma_1_sec
            g_2_sec = self.gamma_2_sec
            weights = self.weights
            weights_sec = self.weights_sec

        g_1 = self._apply_mask(g_1, mask=mask, obj_name='shear 1')
        g_2 = self._apply_mask(g_2, mask=mask, obj_name='shear 2')
        weights = self._apply_mask(weights, mask=mask, obj_name='weights')

        g_1_sec = self._apply_mask(
            g_1_sec, mask=mask_sec, sec=True, obj_name='secondary shear 1')
        g_2_sec = self._apply_mask(
            g_2_sec, mask=mask_sec, sec=True, obj_name='secondary shear 2')
        weights_sec = self._apply_mask(
            weights_sec, mask=mask_sec, sec=True, obj_name='secondary weights')

        return g_1, g_2, g_1_sec, g_2_sec, weights, weights_sec

    def _divide_statistics(self, stats):
        stat_types = {'E': {}, 'B': {}}
        for key in ['shear', 'convergence', 'multi']:
            stats_ = np.asarray(
                list(self.ctx['stat_types'].values())) == key
            stats_ = np.asarray(
                list(self.ctx['stat_types'].keys()))[stats_]
            stat_types['E'][key] = []
            stat_types['B'][key] = []
            for stat in stats_:
                if stat in stats['E']:
                    stat_types['E'][key].append(stat)
                if stat in stats['B']:
                    stat_types['B'][key].append(stat)
        return stat_types

    def _prep_alms(self, pol, mask, mask_sec, trimmed_mask, trimmed_mask_sec,
                   copy_obj, use_shear_maps, sign_flip=True):

        sign_flip = True

        if use_shear_maps:
            g_1, g_2, g_1_sec, g_2_sec, weights, weights_sec = \
                self._prep_shear_maps(mask, mask_sec, copy_obj)

            # calculate spherical harmonics
            vprint(
                "Calculating spherical harmonics "
                "decomposition of shear maps for polarization {}".format(
                    pol),
                logger=self.logger, verbose=self.verbose)

            if sign_flip & (len(g_1) > 0):
                vprint("Applying sign flip", logger=self.logger,
                       verbose=self.verbose)
                g_1[g_1 > hp.UNSEEN] *= -1.
            alm = utils._calc_alms(g_1, g_2, mode=pol,
                                   logger=self.logger,
                                   verbose=self.verbose)
            if sign_flip & (len(g_1) > 0):
                g_1[g_1 > hp.UNSEEN] *= -1.

            if sign_flip & (len(g_1_sec) > 0):
                g_1_sec[g_1_sec > hp.UNSEEN] *= -1.
            alm_sec = utils._calc_alms(
                g_1_sec, g_2_sec, mode=pol,
                logger=self.logger, verbose=self.verbose)
            if sign_flip & (len(g_1_sec) > 0):
                g_1_sec[g_1_sec > hp.UNSEEN] *= -1.
        else:
            alm = []
            alm_sec = []
            if copy_obj:
                weights = copy.copy(self.weights)
                weights_sec = copy.copy(self.weights_sec)
            else:
                weights = self.weights
                weights_sec = self.weights_sec

        weights = self._apply_mask(
            weights, mask=trimmed_mask, obj_name='weights', trimming=True)
        weights_sec = self._apply_mask(
            weights_sec, mask=trimmed_mask_sec, obj_name='secondary weights',
            trimming=True, sec=True)
        return alm, alm_sec, weights, weights_sec

    def _calc_multi_stats(self, outs, scales, plugins, alm,
                          alm_sec, weights, weights_sec,
                          trimmed_mask, trimmed_mask_sec,
                          defined_parameters,
                          undefined_parameters, output_dir,
                          stats, pol,
                          write_to_file, name, copy_obj, statistics):
        for scale in scales:
            self.ctx['scale'] = scale
            vprint("Calculating {} statistics for convergence map "
                   "smoothed with a Gaussian kernel with FWHM {} "
                   "arcmin".format(stats, scale),
                   logger=self.logger, verbose=self.verbose)
            if len(alm) == 0:
                if (pol == 'E') & (len(self.kappa_E) == 0):
                    self.convert_shear_to_convergence()
                if (pol == 'B') & (len(self.kappa_B) == 0):
                    self.convert_shear_to_convergence()
                if pol == 'E':
                    if scale > 0.0:
                        kappa = np.asarray(
                            hp.smoothing(
                                self.kappa_E,
                                fwhm=np.radians(float(scale) / 60.)),
                            dtype=self.ctx['prec'])
                    else:
                        kappa = copy.copy(self.kappa_E)
                elif pol == 'B':
                    if scale > 0.0:
                        kappa = np.asarray(
                            hp.smoothing(
                                self.kappa_B,
                                fwhm=np.radians(float(scale) / 60.)),
                            dtype=self.ctx['prec'])
                    else:
                        kappa = copy.copy(self.kappa_B)
                vprint("Using convergence maps directly",
                       logger=self.logger, verbose=self.verbose)
            else:
                kappa = self._convert_alm_to_kappa(alm, scale)
                vprint("Converted shear maps to convergence maps",
                       logger=self.logger, verbose=self.verbose)

            if len(alm_sec) == 0:
                if (pol == 'E') & (len(self.kappa_E_sec) == 0):
                    self.convert_shear_to_convergence(sec=True)
                if (pol == 'B') & (len(self.kappa_B_sec) == 0):
                    self.convert_shear_to_convergence(sec=True)
                if pol == 'E':
                    if len(self.kappa_E_sec) > 0:
                        if scale > 0.0:
                            kappa_sec = np.asarray(hp.smoothing(
                                self.kappa_E_sec,
                                fwhm=np.radians(float(scale) / 60.)),
                                dtype=self.ctx['prec'])
                        else:
                            kappa_sec = copy.copy(self.kappa_E_sec)
                    else:
                        kappa_sec = []
                elif pol == 'B':
                    if len(self.kappa_B_sec) > 0:
                        if scale > 0.0:
                            kappa_sec = np.asarray(hp.smoothing(
                                self.kappa_B_sec,
                                fwhm=np.radians(float(scale) / 60.)),
                                dtype=self.ctx['prec'])
                        else:
                            kappa_sec = copy.copy(self.kappa_B_sec)
                    else:
                        kappa_sec = []
                vprint("Using convergence maps directly",
                       logger=self.logger, verbose=self.verbose)
            else:
                kappa_sec = self._convert_alm_to_kappa(
                    alm_sec, scale)
                vprint("Converted shear maps to convergence maps",
                       logger=self.logger, verbose=self.verbose)

            kappa = self._apply_mask(
                kappa, mask=trimmed_mask, trimming=True,
                obj_name='smoothed convergence {}-modes'.format(pol))
            kappa_sec = self._apply_mask(
                kappa_sec, mask=trimmed_mask_sec, trimming=True, sec=True,
                obj_name='secondary smoothed convergence {}-modes'.format(pol))

            for statistic in stats:
                if 'Cross' in statistic:
                    stat_out = plugins[statistic](
                        copy.copy(kappa), copy.copy(kappa_sec),
                        copy.copy(weights), copy.copy(weights_sec),
                        self.ctx)
                else:
                    stat_out = plugins[statistic](
                        copy.copy(kappa), copy.copy(weights), self.ctx)
                outs = self._stack_stats(
                    stat_out, pol, statistic, statistics, outs,
                    False, name, output_dir,
                    defined_parameters, undefined_parameters)
        if write_to_file:
            # saving all scales at once
            for statistic in stats:
                output_path = paths.create_path(
                    name,
                    output_dir, {
                        **defined_parameters,
                        **{'mode': pol,
                           'stat': statistic}},
                    undefined_parameters,
                    suffix='.npy')
                if os.path.exists(output_path):
                    out_file = np.load(output_path)
                    out_file = np.vstack(
                        (out_file, outs[pol][statistic]))
                else:
                    out_file = outs[pol][statistic]
                np.save(output_path, out_file)
            return {}
        return outs
