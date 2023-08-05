# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import frogress
import copy
import matplotlib.pyplot as plt
from estats import utils
# import treecorr

from ekit import paths as paths
from ekit import context
from ekit.logger import vprint


class summary:
    """
    The summary module is meant to postprocess summary statistics measurements.

    The main functionality of the summary module is to calculate mean
    data-vectors, standard deviations and covariance or precision matrices
    for the summary statistics at different parameter configurations,
    based on a set of realizations of the summary statistic at each
    configuration.

    The meta data (e.g. cosmology setting, precision settings, tomographic
    bin and so on) for each set of realizations (read-in from a file or an
    array directly) can be
    given to the module on read-in directly or parsed from the filename.
    Directly after read-in a first postprocessing can be done using the process
    function defined in the statistic plugin.
    The read-in data-vectors are stored appended to a data table for each
    statistic and the meta data is added to an internal meta data table.
    The realizations are ordered according to their meta data entry. There
    are two special entries for the meta data (tomo: label for the tomographic
    bin of the data-vectors, NREALS: the number of data-vectors associated to
    each entry (is inferred automatically)).
    All other entries can be defined by the user.

    The summary module allows to downbin the potentially very long data-vectors
    into larger bins using a binning scheme.
    The decide_binning_scheme function in the statistic plugin is used to
    decide on
    that scheme, which defines the edges of the large bins based on the bins
    of the original data-vectors. For plotting purposes the binning scheme
    can also define the values of each data bin (for example its
    signal-to-noise ratio).
    The slice function in the statistic plugin then defines how exactly
    the binning scheme is used to downbin each data-vector.
    See the :ref:`own_stat` Section for more details.

    The summary module allows to combine summary statistics calculated for
    different tomographic bins
    to perform a tomographic analysis. The tomo entry in the meta data table
    defines the label of the tomographic bin for each set of data-vector
    realizations. One can define the order of the labels when combined into
    a joint data-vector using the cross_ordering keyword.

    The summary module also allows to combine different summary
    statistics into a joint data-vector.

    The most important functionalities are:

    - generate_binning_scheme:

        Uses the decide_binning_scheme function from the statistic plugin to
        create a binning scheme. The scheme can be created for different
        tomographic bins and scales.
        See the Section :ref:`own_stat` for more details.

    - readin_stat_files:

        Reads in data-vector realizations from a file. The process function
        from the statistics plugin is used to perform a first processing of
        the data. The meta data for each file can either be given directly or
        can be parsed from the file name by giving a
        list of parameters indicating the fields to be parsed (using ekit).

    - downbin_data:

        Uses the created binning scheme to bin the data-vector entries into
        larger bins.
        Uses the slice function from the statistics plugin to do so.

    - join_redshift_bins:

        Joins all data-vector realizations of a specific statistic at the same
        configuration. The tomo entry in the meta data table
        defines the label of the tomographic bin for each set of data-vector
        realizations. One can define the order of the labels when combined into
        a joint data-vector
        using the cross_ordering keyword. If for a specific parameter
        configuration different number of realizations are found for different
        tomographic bins, only the minimum number of realizations is used to
        calculate the combined data-vectors.

    - join_statistics:

        Creates a new statistic entry including the data table and the meta
        data table, by concatenating the data-vectors of a set of statistics.
        The new statistic has the name statistic1-statistic2-...
        If for a specific parameter configuration
        different number of realizations are found for different statistics,
        only the minimum number of realizations is used to calculate the
        combined data-vectors.

    - get_means:

        Returns the mean data vectors of a statistic for the different
        parameter configurations.

    - get_meta:

        Returns the full meta data table for a statistic.

    - get_errors:

        Returns the standard deviation of the data vectors of a statistic
        for the different configurations.

    - get_covariance_matrices:

        Returns the covariance matrices estimated from the realizations at
        each configuration. Can also invert the covariance matrices directly
        to obtain the precision matrices.

    The accepted keywords are:

    - cross_ordering:

        default: []

        choices: a list of labels

        Indicates the order of the tomographic bin labels that is used by
        join_redshift_bins
        to combine data-vectors from different tomographic bins.

        The labels could be bin1xbin2 for example, and the corresponding
        cross_ordering could be [1x1, 1x2, 2x2, 2x3, 3x3].
    """

    def __init__(self, context_in={}, logger=None, verbose=False, **kwargs):
        """
        Initialization function.

        :param context_in: Context instance
        :param logger: Logging instance
        :param verbose: Verbosity switch
        """
        self.verbose = verbose
        self.logger = logger

        vprint("Initialized summary object with no data so far. \
                Waiting for readin...",
               logger=self.logger, verbose=self.verbose)

        allowed = ['cross_ordering']
        defaults = [[]]
        types = ['list']

        allowed, types, defaults = utils.get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            logger=self.logger, verbose=self.verbose)

        self.meta = {}
        self.data = {}
        self.bin_centers = {}
        self.bin_edges = {}

    # ACCESING OBJECTS
    def get_data(self, statistic='Peaks', params=None):
        """
        Get full data array for a certain statistic

        :param statistic: Statistic for which to return data array
        :param params: Can provide dictionary of parameter values.
        Returns only realisations with those parameters.
        :return : All data vector realisations for the statistic
        """

        if statistic == 'all':
            return self.data
        else:
            if params is not None:
                check = [True] * self.meta[statistic].shape[0]
                for item in params.items():
                    item_row = np.where(
                        np.asarray(self.parameters) == item[0])[0]
                    check &= np.isclose(
                        self.meta[statistic][:, item_row].astype(
                            type(item[1])).reshape(-1), item[1])
                ids = np.where(check)[0]
                out = np.zeros((0, self.data[statistic].shape[1]))
                for id in ids:
                    if id == 0:
                        start = 0
                    else:
                        start = int(np.sum(self.meta[statistic][:id, 1]))
                    end = start + int(np.asarray(self.meta[statistic])[id, 1])
                    out = np.vstack((out, self.data[statistic][start:end]))
            else:
                out = self.data[statistic]
            return np.asarray(out)

    def get_meta(self, statistic='Peaks'):
        """
        Get full meta table for a certain statistic

        :param statistic: Statistic for which to return meta data
        :return : Full meta table for the statistic
        """
        dtype = []
        for ii in self.meta[statistic][0, :]:
            try:
                _ = float(ii)
                dtype.append('f8')
                continue
            except ValueError:
                pass
            try:
                _ = int(ii)
                dtype.append('i4')
                continue
            except ValueError:
                pass
            dtype.append('<U3')
        fields = []
        for line in self.meta[statistic]:
            fields.append(tuple(line))
        dtype = np.dtype({'names': tuple(self.parameters),
                          'formats': tuple(dtype)})
        to_return = np.core.records.fromrecords(fields, dtype=dtype)
        return to_return

    def get_binning_scheme(self, statistic='Peaks', bin=0):
        """
        Get binning scheme for a certain statistic and tomographic bin

        :param statistic: Statistic for which to return the binning scheme
        :param bin: Tomographic bin for which to return the binning scheme
        :return : bin edges and bin centers
        """
        return (self.bin_edges[bin][statistic],
                self.bin_centers[bin][statistic])

    # CLEARING OBJECTS
    def clear_data(self):
        """
        Clear data
        """
        self.data = {}
        vprint("Data cleared", logger=self.logger, verbose=self.verbose)

    def clear_meta(self):
        """
        Clear meta array
        """
        self.meta = {}
        vprint("Meta data cleared", logger=self.logger, verbose=self.verbose)

    def clear_binning_scheme(self):
        """
        Clear binning scheme
        """
        self.bin_centers = {}
        self.bin_edges = {}
        vprint("Bin centers and bin edges cleared",
               logger=self.logger, verbose=self.verbose)

    # SETTING OBJECTS
    def set_data(self, data, statistic='Peaks'):
        """
        Set full data array

        :param data: Data array to set
        :param statistic: The statistic for which to set the data
        """
        self.data[statistic] = data

    def set_meta(self, meta, statistic='Peaks', parameters=[]):
        """
        Set meta array

        :param meta: Meta array to set
        :param statistic: The statistic for which to set the meta data
        :param parameters: A list indicating the parameter labels in the meta
                           data table
        """
        self.meta[statistic] = meta
        self.parameters = parameters

    def set_binning_scheme(self, bin_centers, bin_edges,
                           statistic='Peaks', bin=0):
        """
        Set binning scheme

        :param bin_centers: Centers of the bins to set (only used for plotting)
        :param bin_edges: Edges of the bins to set
        :param statistic: The statistic for which to set the binning scheme
        :param bin: The tomographic bin for which to set the binning scheme
        """
        try:
            self.bin_centers[bin][statistic] = bin_centers
            self.bin_edges[bin][statistic] = bin_edges
        except KeyError:
            self.bin_centers[bin] = {}
            self.bin_edges[bin] = {}
            self.bin_centers[bin][statistic] = bin_centers
            self.bin_edges[bin][statistic] = bin_edges

    def readin_stat_files(self, files, statistic='Peaks', meta_list=[],
                          parse_meta=False, parameters=[]):
        """
        Reads in and does a first processesing of a list of filepaths.

        :param files: A list of files containing the realisations for different
                      parameter configurations
        :param statistic: The name of the statistic to which the files belong
        :param meta_list: Can provide a list for the meta data of the shape
                          (num_of files, num_of_parameters)
        :param parse_meta: If set to True will try to get meta
                           parameters from file names (names need to be in
                           ekit format)
        :param parameters: List of strings indicating the parameter names that
                           should be extracted from the file names
        """
        if type(files) is str:
            files = [files]
        if len(files) == 0:
            return

        for ii, file in frogress.bar(enumerate(files)):
            data = np.load(file)
            self.readin_stat_data(data, statistic=statistic,
                                  meta_list=meta_list,
                                  parse_meta_from_file_names=parse_meta,
                                  parameters=parameters, file=file)
        vprint("Completed readin of {} files for statistic {}".format(
            len(files), statistic), logger=self.logger, verbose=self.verbose)
        self._sort_data(statistic, copy.copy(parameters))

    def rescale_data(self, statistic='Peaks'):
        """
        Devides each databin by the median of the samples.
        Useful when performing SVD for example.
        """
        self.data[statistic] /= np.median(self.data[statistic], axis=0)

    def readin_stat_data(self, data, statistic='Peaks', meta_list=[],
                         parse_meta_from_file_names=False, parameters=[],
                         file=''):
        """
        Processesing of a chunk of realisations belonging to the same parameter
        configuration.

        :param data: An array containing the realisations as
                     (n_reals, length of datavectors)
        :param statistic: The name of the statistic to which the realisations
                          belong
        :param meta_list: Can provide a list for the meta data of the shape
                          (1, num_of_parameters)
        :param parse_meta_from_file_names: If set to True will try to get meta
                                           parameters from file name passed by
                                           file (name need to be in ekit
                                           format)
        :param parameters: List of strings indicating the parameter names that
                           should be extracted from the file name
        :param file: A path from which the meta data can be parsed
        """
        data = self._process_data(
            data, statistic)
        meta = self._get_meta(
            data, meta_list, parse_meta_from_file_names,
            parameters, file_name=file)
        # stacking
        try:
            self.meta[statistic] = np.vstack((self.meta[statistic], meta))
        except KeyError:
            self.meta[statistic] = meta

        try:
            self.data[statistic] = np.vstack((self.data[statistic], data))
        except KeyError:
            self.data[statistic] = data

        self._sort_data(statistic, copy.copy(parameters))

    # METHODS

    def generate_binning_scheme(self, statistics=['Peaks', 'Voids', 'CLs',
                                                  'Minkowski', '2PCF', '2VCF'],
                                bin=0):
        """
        Generates a binning scheme for different statistics for a given
        tomographic bin.

        :param statistics: A list of statistics for which to compute the
                           binning scheme
        :param bin: The tomographic bin for which to calculate the binning
                    scheme
        """
        if isinstance(statistics, str):
            statistics = [statistics]

        for stat in statistics:
            if ('-' in stat):
                vprint('Cannot make binning scheme \
                        for joined statistics. Skipping...',
                       logger=self.logger, verbose=True, level='warning')
                continue

            bin_centers, bin_edges = self._decide_on_bins(
                stat, bin, logger=None)

            try:
                self.bin_centers[bin][stat] = bin_centers
                self.bin_edges[bin][stat] = bin_edges
            except KeyError:
                self.bin_centers[bin] = {}
                self.bin_edges[bin] = {}
                self.bin_centers[bin][stat] = bin_centers
                self.bin_edges[bin][stat] = bin_edges

    def downbin_data(self, statistics=['Peaks', 'Voids', 'CLs',
                                       'Minkowski', '2PCF', '2VCF']):
        """
        Use binning scheme to downbin data vectors into larger bins.

        :param statistics: The statistics for which to perform the binning
        """
        if isinstance(statistics, str):
            statistics = [statistics]
        for stat in statistics:
            vprint("Downbinning data for statistic {}".format(
                stat), logger=self.logger, verbose=self.verbose)
            self._slice_data(errors=[], stat=stat, logger=None)

    def join_statistics(self, statistics=['Peaks', 'CLs']):
        """
        Join datavectors for different statistics. Creates a new instance for
        meta and data objects with the key as the single statistics
        concatinated by '-'s.

        :param statistics: The statistics which should be combined.
        """
        block_sizes = np.zeros(0, dtype=np.int16)
        for entry in range(self.get_meta(statistics[0]).shape[0]):
            # get block size for each entry
            blocks = np.zeros(0)
            for s in statistics:
                blocks = np.append(blocks,
                                   int(self.get_meta(s)['NREALS'][entry]))
            block_sizes = np.append(block_sizes, int(np.min(blocks)))

        # set the new meta array
        self.meta['-'.join(statistics)] = copy.copy(
            self.meta[statistics[0]])
        self.meta['-'.join(statistics)][:, 1] = block_sizes.reshape(-1)

        # get combined data vector lengths, and set collector array
        block_lengths = np.zeros(0, dtype=np.int16)
        for s in statistics:
            block_lengths = np.append(block_lengths, self.data[s].shape[1])
        self.data['-'.join(statistics)
                  ] = np.zeros((np.sum(block_sizes), np.sum(block_lengths)))

        # combine data
        vertical_pointer = 0
        for entry in range(self.get_meta(statistics[0]).shape[0]):
            start = vertical_pointer
            end = vertical_pointer + block_sizes[entry]

            horizontal_pointer = 0
            for ss, stat in enumerate(statistics):
                block_start = horizontal_pointer
                block_end = horizontal_pointer + block_lengths[ss]

                to_p = self.data[stat][int(np.sum(
                    self.get_meta(stat)['NREALS'][:entry].astype(int))):
                    int(np.sum(
                        self.get_meta(stat)['NREALS'][:entry].astype(int)))
                    + block_sizes[entry], :]

                self.data['-'.join(statistics)][start:end,
                                                block_start:block_end] = to_p
                horizontal_pointer = block_end
            vertical_pointer += block_sizes[entry]

        vprint("Constructed joined statistic {}".format(
            '-'.join(statistics)), logger=self.logger, verbose=self.verbose)

    def join_redshift_bins(self):
        """
        Concatenates datavector realisations for the different tomographic
        bins. The old single bin entries get deleted and the new entries have
        tomographic bin set to -1.
        """
        for statistic in self.data.keys():
            bins = np.unique(self.get_meta(statistic)['tomo'])
            # if only one bin do nothing
            if len(bins) == 1:
                vprint(
                    "Cannot join tomographic bins since all samples have "
                    "same tomographic bin", logger=self.logger,
                    verbose=True, level='warning')
                return
            if len(self.ctx['cross_ordering']) > 0:
                bins_ = self.ctx['cross_ordering']
                new_bins = []
                for bin in bins_:
                    if bin in bins:
                        new_bins.append(bin)
                bins = new_bins
            else:
                vprint("Did not find cross_ordering entry. "
                       "Trying to guess the order of the tomographic bins.",
                       verbose=True, level='warning', logger=self.logger)

            bin_idxs = {}
            for bin in bins:
                idx = np.where(self.get_meta(statistic)['tomo'] == bin)[0]
                bin_idxs[bin] = idx

            # reduce all data blocks to same length (in case some contain
            # more noise realisations than others)
            block_sizes = np.zeros(0, dtype=np.int)
            for entry in range(bin_idxs[list(bin_idxs.keys())[0]].size):
                # get maximum block size for each entry
                blocks = np.zeros(0)
                for bin in bins:
                    try:
                        blocks = np.append(blocks, int(
                            self.get_meta(
                                statistic)['NREALS'][bin_idxs[bin]][entry]))
                    except IndexError:
                        raise Exception(
                            "Cannot join redshift bins as not all "
                            "configurations exist for each bin.")
                block_sizes = np.append(block_sizes, int(np.min(blocks)))

            # combine data
            single_block_length = self.data[statistic].shape[1]
            temp_data = np.zeros(
                (int(np.sum(block_sizes)), single_block_length * len(bins)))
            vertical_pointer = 0
            # loop over all blocks
            for entry in range(block_sizes.size):
                # set start and end in new data array
                start = vertical_pointer
                end = vertical_pointer + int(block_sizes[entry])
                # loop over tomographic bins
                for ii in range(len(bins)):
                    pos = bin_idxs[bins[ii]][entry]
                    # set start and end for old data array
                    low = int(
                        np.sum(
                            self.get_meta(
                                statistic)['NREALS'][:pos].astype(int)))
                    high = low + int(block_sizes[entry])
                    temp_data[start:end, ii * single_block_length:(
                        ii + 1) * single_block_length]\
                        = self.data[statistic][low:high, :]
                # update start position for new data array
                vertical_pointer = end

            # update class object
            self.data[statistic] = temp_data

            # update meta
            self.meta[statistic] = self.meta[statistic][
                bin_idxs[list(bin_idxs.keys())[0]], :]
            self.meta[statistic][:, 0] = -1
            self.meta[statistic][:, 1] = block_sizes.reshape(-1)

            vprint("Joined data from tomographic bins for statistic {}. "
                   "The order is {}".format(statistic, bins),
                   logger=self.logger, verbose=self.verbose)

    def get_means(self, statistic='Peaks'):
        """
        Returns the mean datavectors for all different parameter
        configurations for a given statistic.

        :param statistic: Statistic for which to return means
        :return : An array containing the mean data vectors as
                  (number of parameter configurations, data vector length)
        """
        pointer = 0
        means = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            means[ii, :] = np.nanmean(
                self.data[statistic][pointer:pointer + int(entry[1]), :],
                axis=0)
            pointer += int(entry[1])
        return means

    def get_errors(self, statistic='Peaks'):
        """
        Returns the error datavectors for all different parameter
        configurations for a given statistic.

        :param statistic: Statistic for which to return errors
        :return: An array containing the error data vectors as
                (number of parameter configurations, data vector length)
        """
        pointer = 0
        errors = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            errors[ii, :] = np.nanstd(
                self.data[statistic][pointer:pointer + int(entry[1]), :],
                axis=0)
            pointer += int(entry[1])
        return errors

    def get_covariance_matrices(self, statistic='Peaks', invert=False,
                                set_to_id_if_failed=False,
                                plot_fiducial_correlation=False,
                                plot_fiducial_incov=False,
                                Fiducials=[]):
        """
        Returns the covariance matrices for all different parameter
        configurations for a given statistic.

        :param statistic: Statistic for which to return errors
        :param invert: If True attempts to invert the covariance matrices.
                       If numerically unstable raises Error
        :param set_to_id_if_failed: If True sets matrices to identity matrix
                                    if the inversion fails.
        :param plot_fiducial_correlation: If True plots the correlation matrix
                                          and covariance matrix
                                          for the fiducial parameter setting
                                          indicated by Fiducials
        :param plot_fiducial_incov: If True plots the inverted covariance
                                    matrix for the fiducial parameter setting
                                    indicated by Fiducials
        :param Fiducials: The fiducial parameter values for which to plot
        :return : An array containing the (inverted) covariance matrices as
                  (number of parameter configurations, data vector length,
                  data vector length)
        """
        covs = self._calc_cov_matrices(
            statistic, invert, set_to_id_if_failed,
            plot_fiducial_correlation,
            plot_fiducial_incov,
            Fiducials)
        return covs

    def get_full_summary(self, statistic='Peaks', invert=False,
                         set_to_id_if_failed=False,
                         plot_fiducial_correlation=False,
                         plot_fiducial_incov=False,
                         Fiducials=[],
                         label='', reorder=False,
                         check_stability=False, calc_covs=True):
        """
        Returns the mean datavectors, errors and (inverted) covariance matrices
        for all different parameter configurations for a given statistic.

        :param statistic: Statistic for which to return errors
        :param invert: If True attempts to invert the covariance matrices.
                       If numerically unstable raises Error
        :param set_to_id_if_failed: If True sets matrices to identity matrix
                                    if the inversion fails.
        :param plot_fiducial_correlation: If True plots the correlation matrix
                                          and covariance matrix
                                          for the fiducial parameter setting
                                          indicated by Fiducials
        :param plot_fiducial_incov: If True plots the inverted covariance
                                    matrix for the fiducial parameter setting
                                    indicated by Fiducials
        :param Fiducials: The fiducial parameter values for which to plot
        :param label: Label used to create path for cov and corr matrix plots
        :param reorder: (DEPREACATED) If True attempts to reorder data vectors
        :param check_stability: If True performs numerical stability checks
                                when inverting covariance matrices
        :param calc_covs: Can turn off the calculation of covariance matrices.
                          For example when SVD should be used.
        :return: 3 objects. Means, errors and (inverted) covariance matrices
        """

        errors = self.get_errors(statistic)
        means = self.get_means(statistic)

        # optionally reorder from [[scale 1], ..., [scale n]]
        # to [[bin 1], ..[bin m]]
        if reorder:
            pass
            # self._reorder()
            # errors = self.get_errors(statistic)
            # means = self.get_means(statistic)

        if calc_covs:
            covs = self._calc_cov_matrices(
                statistic, invert, set_to_id_if_failed,
                plot_fiducial_correlation,
                plot_fiducial_incov,
                Fiducials, label, check_stability)
        else:
            covs = []
        return (means, errors, covs)

    ##################################
    # HELPER FUNCTIONS
    ##################################

    def _reorder(self):
        """
        DEPRECATED
        """
        for statistic in self.meta.keys():
            if statistic == 'CLs':
                continue
            mult = 1
            if statistic == 'Minkowski':
                mult = 3
            scales = self.ctx['scales']
            bins_per_scale = mult * \
                self.ctx['{}_sliced_bins'.format(statistic)]
            reorder_idx = np.zeros(0)
            for bin in range(bins_per_scale):
                reorder_idx = np.append(
                    reorder_idx,
                    bin + np.arange(len(scales)) * bins_per_scale)

            self.data[statistic] = \
                self.data[statistic][:, reorder_idx.astype(int)]

    def _process_2pt(self, raw_data, statistic, trimmed_mask_dict, num_of_bins,
                     parameters, meta_list=[]):
        """
        (DEPRECATED)
        Used to process the coordinates of the extreme
        value stats into correlation function.
        """
        meta = self._get_meta(raw_data, meta_list, False, parameters)
        try:
            self.meta[statistic] = np.vstack((self.meta[statistic], meta))
        except KeyError:
            self.meta[statistic] = meta
        idx_sort = self._get_sort_idx(parameters, statistic)
        self.meta[statistic] = self.meta[statistic][idx_sort, :]
        output = self._process_2_point_corr(
            raw_data, statistic, trimmed_mask_dict,
            self.ctx['scales'], num_of_bins)
        vprint("Converted extreme value coordinates into real space \
                2 point correlation function",
               logger=self.logger, verbose=self.verbose)
        return output

    def _calc_cov_matrices(self, statistic, invert=False,
                           set_to_id_if_failed=False,
                           plot_fiducial_correlation=False,
                           plot_fiducial_incov=False,
                           Fiducials=[],
                           label='',
                           check_stability=False):
        """
        Calculation and inversion of covariance matrices
        """
        pointer = 0
        covs = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1],
             self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            # calculate covariance matrix
            mask = np.isnan(self.data[statistic]
                            [pointer:pointer + int(entry[1]), :])
            mx = np.ma.masked_array(
                self.data[statistic][pointer:pointer + int(entry[1]), :],
                mask=mask)
            c = np.ma.cov(mx, rowvar=False, allow_masked=True)

            if plot_fiducial_correlation:
                check = True
                for xx, par in enumerate(entry[2:]):
                    check_ = np.isclose(par, Fiducials[xx])
                    check &= check_
                if check:
                    plt.figure(figsize=(12, 8))
                    plt.imshow(np.ma.corrcoef(mx, rowvar=False,
                                              allow_masked=True))
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    cbar = plt.colorbar()
                    cbar.ax.tick_params(labelsize=20)
                    plt.savefig('corr_mat_{}_{}.pdf'.format(statistic, label))
                    plt.clf()

                    plt.figure(figsize=(12, 8))
                    plt.imshow(c)
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    cbar = plt.colorbar()
                    cbar.ax.tick_params(labelsize=20)
                    plt.savefig('cov_mat_{}_{}.pdf'.format(statistic, label))
                    plt.clf()

            if invert:
                try:
                    incov = np.linalg.inv(c)
                except np.linalg.LinAlgError:
                    # Fallback to tricks if inversion not possible
                    if (np.isclose(np.linalg.det(c), 0.0)):
                        vprint(
                            "Determinant close to 0. Trying Inversion tricks",
                            logger=self.logger, verbose=self.verbose)
                        c *= 10e20
                        if (np.isclose(np.linalg.det(c), 0.0)):
                            if set_to_id_if_failed:
                                vprint("Inversion of covariance failed. "
                                       "SETTING PRECISON MATRIX TO IDENTITY",
                                       logger=self.logger,
                                       verbose=True, level='warning')
                                incov = np.identity(c.shape[0])
                            else:
                                raise Exception(
                                    "Error: Fiducial Covariance Matrix \
                                     not invertible!!!")
                        else:
                            incov = np.linalg.pinv(c)
                        incov *= 10e20

                    else:
                        incov = np.linalg.pinv(c)

                # check numerical stability of inversion
                if check_stability:
                    id_check = np.dot(c, incov)
                    id = np.eye(id_check.shape[0])
                    id_check -= id
                    if not np.all(np.isclose(id_check, 0.0, atol=1e10,
                                             rtol=0.0)):
                        raise Exception(
                            "Inversion of Fiducial Covariance matrix "
                            "did not pass numerical stability test")
                    else:
                        vprint("Successfully inverted Fiducial "
                               "Covariance matrix",
                               logger=self.logger, verbose=self.verbose)

                covs[ii] = incov

                if plot_fiducial_incov:
                    check = True
                    for xx, par in enumerate(entry[2:]):
                        check_ = np.isclose(par, Fiducials[xx])
                        check &= check_
                    if check:
                        plt.figure(figsize=(12, 8))
                        plt.imshow(incov)
                        plt.xticks(fontsize=20)
                        plt.yticks(fontsize=20)
                        cbar = plt.colorbar()
                        cbar.ax.tick_params(labelsize=20)
                        plt.savefig(
                            'incov_mat_{}_{}.pdf'.format(statistic, label))
                        plt.clf()
            else:
                covs[ii] = c

            pointer += int(entry[1])
        return covs

    def _get_meta_from_file_name(self, parameters, file):
        """
        Parse meta data from file names
        """
        defined = paths.get_parameters_from_path(file)[0]

        meta = np.zeros(0, dtype=object)
        for param in parameters:
            meta = np.append(meta, defined[param][0])
        return meta

    def _process_data(self, raw_data, stat, trimmed_mask_dict={},
                      logger=None):
        """
        Load a STATS file in the correct format
        """

        plugin = utils.import_executable(stat,
                                         'process',
                                         self.verbose,
                                         self.logger)

        return plugin(raw_data, self.ctx, False)

    def _stack_data(self, raw_data, num_of_scales):
        """
        Stacks data arrays
        """
        data = np.zeros(
            (int(raw_data.shape[0] / num_of_scales), raw_data.shape[1]
             * num_of_scales))
        for jj in range(int(raw_data.shape[0] / num_of_scales)):
            data[jj, :] = raw_data[jj * num_of_scales:
                                   (jj + 1) * num_of_scales, :].ravel()
        return data

    def _get_meta(self, data, meta_list=[], parse_meta_from_file_names=False,
                  parameters=[],
                  file_name=''):
        """
        Helper function to get meta data
        """
        # Setting meta data
        NREALS = int(np.asarray([data.shape[0]]))
        if (len(meta_list) == 0) & (not parse_meta_from_file_names):
            meta = NREALS
        elif not parse_meta_from_file_names:
            meta = np.append(NREALS, meta_list)
        elif parse_meta_from_file_names:
            to_app = self._get_meta_from_file_name(parameters, file_name)
            meta = np.append(NREALS, to_app)

        # put tomographic bin to the beginning
        if 'tomo' in parameters:
            idx = np.asarray(parameters) == 'tomo'
            idx = np.append([False], idx)
            meta[idx] = meta[idx]
            idx = np.where(idx)[0]
            tomo_column = meta[idx]
            meta = np.delete(meta, idx)
            meta = np.append(tomo_column, meta)
        else:
            meta = np.append(np.zeros(1), meta)
        return meta.reshape(1, -1)

    def _get_sort_idx(self, parameters, statistic):
        """
        Performs sorting of meta data
        """
        # lexsort
        idx = np.delete(np.arange(self.meta[statistic].shape[1]), 1)
        sort_idx = np.lexsort(
            np.flip(self.meta[statistic][:, idx], axis=1).transpose())

        return sort_idx

    def _generate_random_points(self, masks, num_objects):
        """
        (DEPRECATED)
        Generates random points on sky for 2pt correlator
        """
        # Calculate number of randoms needed for the mask
        sky_coverage = np.sum(masks[0]) / masks[0].size
        num_randoms = int(num_objects * 1. / sky_coverage)

        # Generate the random points uniformly
        ran_dec = -1.0 + 2. * np.random.random(size=num_randoms)
        ran_ra = 2.0 * np.pi * np.random.random(size=num_randoms)
        ran_dec = np.arccos(ran_dec)

        # convert to pixel values
        pix = hp.pixelfunc.ang2pix(self.ctx['NSIDE'], ran_dec, ran_ra)

        rand_coord = {}
        # remove masked objects
        for cut in masks.keys():
            idx = masks[cut][pix] != 0

            ran_dec_sample = ran_dec[idx]
            ran_ra_sample = ran_ra[idx]

            ran_dec_sample = np.pi / 2. - ran_dec_sample

            ran_dec_sample = np.degrees(ran_dec_sample)
            ran_ra_sample = np.degrees(ran_ra_sample)

            random_coordinates = np.hstack(
                (ran_dec_sample.reshape(-1, 1), ran_ra_sample.reshape(-1, 1)))
            rand_coord[cut] = random_coordinates

        return rand_coord

    def _slice_data(self, errors=[], stat='Peaks', logger=None):
        """
        Given some datavectors and a list of edge indices for the new bins
        as created using decide_on_bins() down-samples the datavectors
        """

        plugin = utils.import_executable(stat,
                                         'slice',
                                         self.verbose,
                                         self.logger)

        num_of_scales, n_bins_sliced, operation, mult = \
            plugin(self.ctx)

        n_bins_original = self.data[stat].shape[1] // (mult * num_of_scales)
        new_data_total = np.zeros(
            (self.data[stat].shape[0], mult * n_bins_sliced * num_of_scales))

        bins = np.unique(self.meta[stat][:, 0])

        for bin in bins:
            # get meta entries for right bin
            bin_idx = np.where(self.meta[stat][:, 0] == bin)[0]

            # select data in the right bin
            idx = np.zeros(self.data[stat].shape[0])
            for ii in bin_idx:
                start = int(np.sum(self.meta[stat][:, 1][:ii].astype(int)))
                end = start + int(self.meta[stat][:, 1][ii])
                idx[start:end] = 1
            idx = idx.astype(bool)

            if operation != 'none':
                new_data = _slicer(
                    data=self.data[stat][idx],
                    num_of_samples=self.data[stat][idx].shape[0],
                    n_bins_original=n_bins_original,
                    n_bins_sliced=n_bins_sliced,
                    bin_edges=self.bin_edges[bin][stat],
                    num_of_scales=num_of_scales,
                    mult=mult, operation=operation)
            else:
                new_data = self.data[stat][idx]

            new_data_total[idx, :] = new_data

        self.data[stat] = new_data_total

        vprint("Down sampled data vectors for statistic {} from {} \
                bins to {} bins".format(
            stat, n_bins_original, n_bins_sliced),
            logger=self.logger, verbose=self.verbose)

    def _decide_on_bins(self, stat, bin=0, logger=None):
        """
        Given some realisations of a datavector decides how to arange
        a fixed number of bins
        """

        plugin = utils.import_executable(stat,
                                         'decide_binning_scheme',
                                         self.verbose,
                                         self.logger)

        try:
            data = self.data[stat]
            meta = self.meta[stat]
        except KeyError:
            data = []
            meta = []
        bin_edge_indices, bin_centers = \
            plugin(data, meta, bin, self.ctx)

        vprint("Decided on binning scheme for statistic {}".format(
            stat), logger=self.logger, verbose=self.verbose)

        return bin_centers, bin_edge_indices

    def _sort_data(self, statistic, parameters):
        """
        Sort data array according to parameters
        """
        idx_sort = self._get_sort_idx(parameters, statistic)

        # sort the blocks in the data
        temp_data = np.zeros_like(self.data[statistic])
        pointer = 0
        for ii in range(self.meta[statistic].shape[0]):
            block_length = int(self.meta[statistic][:, 1][idx_sort[ii]])
            start = int(np.sum(
                self.meta[statistic][:, 1][:idx_sort[ii]].astype(int)))
            end = start + int(block_length)
            to_paste = self.data[statistic][start:end, :]
            temp_data[pointer:pointer + int(block_length), :] = to_paste
            pointer += int(block_length)

        vprint("Sorted the data and meta objects",
               logger=self.logger, verbose=self.verbose)
        # set the objects
        self.data[statistic] = temp_data
        self.meta[statistic] = self.meta[statistic][idx_sort, :]
        self.parameters = ['tomo', 'NREALS']
        parameters.remove('tomo')
        self.parameters += parameters


def _slicer(data, num_of_samples, n_bins_original, n_bins_sliced, bin_edges,
            num_of_scales=1, mult=1, operation='mean', get_std=False):
    """
    Slices data arrays into subbins
    """
    new_data = np.zeros((num_of_samples, mult * n_bins_sliced * num_of_scales))

    for jj in range(num_of_scales):
        # loop over Minkowski functions
        for ii in range(mult):
            # loop over bins
            for xx in range(n_bins_sliced):
                # Slice out correct scale
                to_combine = data[:, int(n_bins_original * (mult * jj + ii)
                                         + bin_edges[jj][xx]):int(
                    n_bins_original * (mult * jj + ii)
                    + bin_edges[jj][xx + 1])]

                if get_std:
                    num = bin_edges[0, xx + 1] - bin_edges[0, xx]
                    fac = 1. / np.sqrt(num)
                else:
                    fac = 1.

                if operation == 'mean':
                    new_data[:, n_bins_sliced
                             * (ii + mult * jj) + xx] = fac \
                        * np.nanmean(to_combine, axis=1)
                elif operation == 'sum':
                    new_data[:, n_bins_sliced
                             * (ii + mult * jj) + xx] = fac \
                        * np.nansum(to_combine, axis=1)
    return new_data

    # def _process_2_point_corr(self, data, stat, num_of_bins,
    #                             trimmed_mask_dict, max_sep):
    #    """
    #    Not maintained
    #    """
    #    tomo_bins = np.unique(self.meta[stat][:, 0])
    #    num_of_scales = len(self.ctx['scales'])

    #    for bin in tomo_bins:
    #        rand_coords = self._generate_random_points(
    #            trimmed_mask_dict[bin],
    #  self.meta[stat][np.equal(self.meta[stat][:, 0], bin), 1][-1])

    #        # Load random points for each cutout
    #        random_ra = {}
    #        random_dec = {}
    #        for cutout in range(trimmed_mask_dict[bin].keys()):
    #            random_ra[cutout] = rand_coords[bin][cutout][:, 1]
    #            random_dec_proto = rand_coords[bin][cutout][:, 0]
    #            random_dec[cutout] = random_dec_proto
    #        vprint("Randoms read")

    #        # read in the data and randoms
    #        data_ra = data[:, 1]
    #        data_dec = data[:, 0]
    #        vprint("Data read")

    #        # determine the number of samples in the data catalog
    #        separators = np.where(np.all(np.isclose(data, -999.0), axis=1))[0]
    #        num_of_pieces = len(separators)
    #        num_of_samples = int(num_of_pieces / num_of_scales)
    #        data_separators = np.append([-1], separators)

    #        if len(data_separators) == 0:
    #            raise Exception(
    #                "No file found that requires processing. Stopping")

    #        output = np.zeros((num_of_samples, num_of_scales * num_of_bins))
    #        for sample_ii in range(num_of_samples):
    #            vprint("Running on sample {} out of {} samples".format(
    #                sample_ii + 1, num_of_samples))

    #            cutout = sample_ii % len(trimmed_mask_dict[bin].keys())

    #            # 2-point correlation function for random catalog
    #            random_cat = treecorr.Catalog(
    #                ra=random_ra[cutout], dec=random_dec[cutout],
    #              ra_units='deg', dec_units='deg')

    #            for fwhm_ii in range(num_of_scales):
    #                # 2-point correlation function for catalog
    #                sample_ra = data_ra[data_separators[sample_ii *
    # num_of_scales +
    #                                                    fwhm_ii] + 1:
    # data_separators[sample_ii * num_of_scales + fwhm_ii + 1]]
    #                sample_dec = data_dec[data_separators[sample_ii *
    # num_of_scales +
    #                                                      fwhm_ii]
    # + 1:data_separators[sample_ii * num_of_scales + fwhm_ii + 1]]
    #                data_cat = treecorr.Catalog(
    #                    ra=sample_ra, dec=sample_dec, ra_units='deg',
    # dec_units='deg')

    #                # building the trees
    #                min_sep = float(self.ctx['scales'][fwhm_ii]) * 2.
    #                nn = treecorr.NNCorrelation(
    #                    min_sep=min_sep, max_sep=max_sep, nbins=num_of_bins,
    # sep_units='arcmin')
    #                rr = treecorr.NNCorrelation(
    #                    min_sep=min_sep, max_sep=max_sep, nbins=num_of_bins,
    # sep_units='arcmin')
    #                nr = treecorr.NNCorrelation(
    #                    min_sep=min_sep, max_sep=max_sep, nbins=num_of_bins,
    # sep_units='arcmin')
    #                rn = treecorr.NNCorrelation(
    #                   min_sep=min_sep, max_sep=max_sep, nbins=num_of_bins,
    # sep_units='arcmin')

    #                # Run correlators
    #                nn.process(data_cat)
    #                rr.process(random_cat)
    #                nr.process(data_cat, random_cat)
    #                rn.process(random_cat, data_cat)

    #                # using Landy Szalay to calculate the 2PT
    #                xi, var_xi = nn.calculateXi(rr, nr, rn)

    #                output[sample_ii, num_of_bins * fwhm_ii:num_of_bins *
    #                       (fwhm_ii + 1)] = xi.reshape(1, -1)

    #        return output


def _get_border(data, min_count):
    """
    Helper function to decide on binning scheme
    """
    check_E = np.cumsum(data, axis=1)
    idE = np.zeros_like(check_E)
    idE[check_E >= float(min_count)] = 1
    idE = np.gradient(idE, axis=1)
    try:
        ext_bin = np.max(np.where(idE > 0.01)[1], axis=0) + 1
    except ValueError:
        ext_bin = 1
    return ext_bin
