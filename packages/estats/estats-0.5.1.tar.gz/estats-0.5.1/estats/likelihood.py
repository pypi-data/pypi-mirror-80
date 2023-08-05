# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
from scipy.interpolate import LinearNDInterpolator, CloughTocher2DInterpolator
from scipy.interpolate import SmoothBivariateSpline
from ekit import context
from ekit.logger import vprint
import scipy
import scipy.special
from estats import utils


class likelihood:

    """
    Class meant to perform parameter inference based on predictions
    of the data-vectors and covariance matrices at different parameter
    configurations.

    The main functionality is calculate the negative logarithmic likelihood at
    a given parameter configuration given a measurement data-vector.

    The parameter space is broken down into two parts called parameters and
    nuisances, that are treated differently.

    To obtain the data-vector and precision matrix predictions at the different
    parameter configurations a full interpolation is used. This requires a
    sufficiently dense sampling of the parameter space.

    The nuisance parameter space is treated as an extension and an emulator is
    built for this part of the configuration space. Therefore, the part of the
    configuration space that is associated to the nuisance parameters requires
    less dense sampling.
    There is a hard-coded emulator when using the parameters as Om, s8 and
    nuisances IA, m, z. This emulator is described in Zuercher et al. 2020.
    Otherwise, a piecewise spline for each nuisance parameter is fit
    individually. Note that this assumes that each nuisance parameter is
    sufficiently independent
    of the other nuisance parameters and also the parameters.

    On read-in of the data used to build the interpolator and emulator the
    given covariance matrices are inverted to obtain the precision matrices.
    This inversion can be numerically unstable for very large matrices or ill
    behaved entries. Therefore, one can use the filter function defined in the
    statistic plugin to decide which data bins to use exactly in the inference
    or to leave out scales when using a multiscale data-vector for example.
    Additionally, a Singular-Value-Decomposition can be used to further reduce
    the length of the data-vectors and the dimensionality of the matrices.

    The most important functionalities are:

    - readin_interpolation_data:

        Loads data used for interpolation. The data is expected to be in a
        format as used by the estats.summary module. Can apply the filter
        function and/or the Singular-Value-Decomposition.

    - build_interpolator:

        Builds the interpolator for the parameter space used to interpolate
        the expected data-vectors and precision matrices between different
        parameter configurations. There are three different choices
        for the type of interpolator used at the moment.

    - build_emulator:

        Builds the emulators for the nuisance parameters individually for each
        data bin (requires less dense sampling than using a full interpolator).
        There is a hard-coded emulator when using the parameters as Om, s8 and
        nuisances IA, m, z.
        This emulator is described in Zuercher et al. 2020.
        Otherwise, a piecewise spline for each nuisance parameter is fit
        individually.
        Note that this assumes that each nuisance parameter is sufficiently
        independent of the other nuisance parameters and also the parameters.

    - get_neg_loglikelihood:

        Returns negative logarithmic likelihood given a measurement data-vector
        at the location in parameter space indicated.

    The accepted keywords are:

    - statistic:

        default: Peaks

        choices: name of one of the statistic plugins

        Decides which statistic plugin to use. In the likelihood module only
        the filter function is used from the plugin.

    - selected_parameters:

        default: [[0.276], [0.811]]

        choices: A list of parameter configurations.

        Indicates the points in the parameter space where the module searches
        for data-vector realizations in the nuisance space.
        The emulator is built based on samples provided at those parameter
        configurations.

    - parameters:

        default: [Om, s8]

        choices: list of strings

        The names of the parameters to consider

    - parameter_fiducials:

        default: [0.276, 0.811]

        choices: list of floats

        The default values of the parameters.
        Used to decide on the fiducial covariance matrix if no interpolation
        of the covariance matrix is used.

    - nuisances:

        default: [IA, m, z]

        choices: list of strings

        The names of the nuisance parameters to consider

    - nuisance_fiducials:

        default: [0.0, 0.0, 0.0]

        choices: list of floats

        The default values of the nuisance parameters.
        Used to decide on the fiducial covariance matrix if no interpolation
        of the covariance matrix is used.

    - n_tomo_bins:

        default: 3

        choices: integer

        The number of tomographic bins considered. Only needed if the special
        emulator is used or a statistic with the name Cross in it.

    - method:

        default: multi

        choices: linear, cubic, multi

        The type of the interpolator that is used.
        Linear mode fits an N-dimensional, piecewise spline interpolating
        between different data bins.
        Cubic mode uses a 2D cubic, piecewise spline interpolating between
        different data bins. This method works only for two parameters.
        multi mode uses a piecewise spline of arbitrary complexity individually
        for each data bin. This method works only for two parameters.

    - cross_ordering:

        default: []

        choices: a list of labels

        Indicates the order of the tomographic bin labels that is assumed in
        the filter function.

        The labels could be bin1xbin2 for example, and the corresponding
        cross_ordering could be [1x1, 1x2, 2x2, 2x3, 3x3].
    """

    def __init__(self, context_in={}, logger=None, verbose=False, **kwargs):
        """
        Initializes likelihhod instance

        :param context_in: Context instance
        :param logger: Logging instance
        :param verbose: Verbosity switch
        """

        self.verbose = verbose
        self.logger = logger

        vprint("Initializing likelihood object",
               verbose=self.verbose, logger=self.logger)

        # setup context
        types = ['int', 'str', 'list', 'list', 'list',
                 'list', 'list', 'str', 'list', 'list']

        defaults = [3, 'multi',
                    ['Omega0', 'Sigma8'], [0.276, 0.811],
                    ['IA', 'm', 'z'], [0.0, 0.0, 0.0],
                    [['flat', 0.07, 0.55], ['flat', 0.47, 1.2],
                     ['flat', -5.5, 5.5],
                     ['flat', -0.1, 0.1], ['flat', -0.1, 0.1]],
                    'Peaks', [[0.276], [0.811]], []]

        allowed = ['n_tomo_bins', 'method', 'parameters',
                   'parameter_fiducials', 'nuisances', 'nuisance_fiducials',
                   'prior_configuration', 'statistic', 'selected_parameters',
                   'cross_ordering']

        allowed, types, defaults = utils.get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            logger=self.logger, verbose=self.verbose)

        vprint("NOTE: If a list of parameters are given to the get_something"
               "functions the values must be in the same order as given in "
               "the parameters and nuisance keywords",
               verbose=self.verbose, logger=self.logger)

        # Initialize empty objects
        self.MEANS = []
        self.ERRORS = []
        self.INCOVS = []
        self.emulators = {}
        self.interpolator = []
        self.precision_matrix = []
        self.bin_array = []
        self.S_inv = []
        self.V_T_inv = []

    # GET OBJECTS

    def get_meta(self, params=None):
        """
        Access the meta data table

        :param: params: Dictionary or list of paramters for filtering.
        :return: (Filtered) meta data
        """
        if params is None:
            return self.META
        else:
            dict = self._convert_dict_list(params, 'dict')
            idx = self._get_loc(dict)
            return self.META[idx]

    def get_means(self, params=None, use_SVD=False):
        """
        Access the mean data vectors stored.

        :param: params: Dictionary or list of paramters for filtering.
        :param use_SVD: If True applies SVD before returning the data vectors
        :return: (Filtered) means
        """
        if params is None:
            means_ = self.MEANS
        else:
            dict = self._convert_dict_list(params, 'dict')
            idx = self._get_loc(dict)
            means_ = self.MEANS[idx]

        if use_SVD:
            means_ = self.MEANS[idx]
            means = np.zeros((0, len(self._single_SVD(self.MEANS[0]))))
            for m in range(means_.shape[0]):
                means = np.vstack((means,
                                   self._single_SVD(means_[m])))
            return means
        else:
            return means_

    def get_interp_means(self, params, use_SVD=False):
        """
        Predict interpolated datavector at a parameter configuration.

        :param: params: Dictionary or list of paramters for filtering.
        :param use_SVD: If True applies SVD before returning the data vectors
        :return: Interpolated data vector
        """

        list = self._convert_dict_list(params, 'list')
        mean = self._get_interp_data_vector(list, use_SVD)
        return mean

    def get_errors(self, params=None, use_SVD=False):
        """
        Access the errors for each parameter configuartion

        :param: params: Dictionary or list of paramters for filtering.
        :param use_SVD: If True applies SVD before returning
        :return: (Filtered) error data
        """
        if params is None:
            means_ = self.ERRORS
        else:
            dict = self._convert_dict_list(params, 'dict')
            idx = self._get_loc(dict)
            means_ = self.ERRORS[idx]

        if use_SVD:
            raise Exception(
                "Sorry, returning errors in the SVD basis is not supported "
                "yet")
        else:
            return means_

    def get_precision_matrices(self, params=None):
        """
        Access the stored precision matrices

        :param: params: Dictionary or list of paramters for filtering.
        :return: (Filtered) precision matrices
        """

        if len(self.S_inv) > 0:
            vprint(
                "The returned precision matrices are transformed into the "
                "SVD basis", logger=self.logger, verbose=True, level='warning')

        if params is None:
            return self.INCOVS
        else:
            dict = self._convert_dict_list(params, 'dict')
            idx = self._get_loc(dict)
            return self.INCOVS[idx]

    def get_interp_precision_matrix(self, params):
        """
        Access the precision matrix. Interpolated to parameters params

        :param: params: Dictionary or list of paramters for filtering.
        :return: The interpolated precision matrix at the parameter
                 configuration
        """

        if len(self.S_inv) > 0:
            vprint(
                "The returned precision matrix is transformed into the "
                "SVD basis", logger=self.logger, verbose=True, level='warning')

        list = self._convert_dict_list(params, 'list')
        return self._get_interp_precision_matrix(list)

    def get_fiducial_precision_matrix(self):
        """
        If no interpolation of the precision matrix is used. The fiducial one
        is used everywhere. Can get it with this function.
        """
        return self.precision_matrix

    def get_interpolator(self):
        """
        Access the interpolators

        :return: The interpolators for each databin
        """
        if len(self.S_inv) > 0:
            vprint(
                "The returned interpolators are transformed into the "
                "SVD basis", logger=self.logger, verbose=True, level='warning')
        return self.interpolator

    def get_precision_interpolator(self):
        """
        Access the interpolators for the precision matrix

        :return: The interpolators for each element of the precision matrix
        """

        if len(self.S_inv) > 0:
            vprint(
                "The returned interpolators are transformed into the "
                "SVD basis", logger=self.logger, verbose=True, level='warning')

        return self.prec_interpolator

    def get_emulators(self):
        """
        Access the emulators

        :return: The emulator for each bin of the datavector
        """

        return self.emulators

    # CLEAR OBJECTS

    def clear_meta(self):
        """
        Clear meta data table
        """
        self.META = []

    def clear_means(self):
        """
        Clear means
        """
        self.MEANS = []

    def clear_errors(self):
        """
        Clear error table
        """
        self.ERRORS = []

    def clear_covariances(self):
        """
        Clear covariance matrices
        """
        self.INCOVS = []

    def clear_precision_matrix(self):
        """
        Clear precision matrix
        """
        self.precision_matrix = []

    def clear_interpolator(self):
        """
        Clear interpolators
        """
        self.interpolator = []

    def clear_cov_interpolator(self):
        """
        Clear covariance interpolators
        """
        self.interpolator = []

    def clear_emulators(self):
        """
        Clear emulators
        """
        self.emulators = {}

    # SET OBJECTS

    def set_meta(self, meta):
        """
        Set meta data table

        :param meta: Meta table to set
        """
        self.META = meta

    def set_means(self, means, systematics=True,
                  reduce_to_selected_scales=False, use_SVD=False):
        """
        Set mean data vectors

        :param meta: Means to set
        :param systematics: If True capture variance in nuisance parameters
                            as well with the SVD.
        :param reduce_to_selected_scales: If True cuts out all scales from the
                                          multiscale datavector that are not
                                          in ctx[selected_scales].
                                          Based on the filter function in the
                                          statistic plugin.
        :param use_SVD: Reduce dimensionality of data using SVD. Build the
                        transformation products used to perform SVD.
        """

        if len(self.S_inv) > 0:
            raise Exception("Resetting the mean datavectors with SVD already "
                            "performed leads to errorous behaviour.")
        else:
            if reduce_to_selected_scales:
                # create the filter for the data vector
                filter = self._create_filter()
                means = means[:, filter]

            if use_SVD:
                u, s, vh = np.linalg.svd(means, full_matrices=True)

                # Missed variance maximally allowed
                vars = np.cumsum(s**2. / np.sum(s**2.))
                requirement = 0.0000001
                idx = 1. - vars > requirement
                self.SVD_selection = idx
                vprint("SVD performed: Keeping {} % of variance".format(
                    (1. - requirement) * 100.),
                    logger=self.logger, verbose=self.verbose, level='warning')
                vprint("Reduced data vector length from {} to {}".format(
                    means.shape[1], np.sum(idx)),
                    logger=self.logger, verbose=self.verbose, level='warning')
                s = np.diag(s)
                S_inv = np.linalg.inv(s)
                V_T_inv = np.linalg.inv(vh)

                self.S_inv = S_inv
                self.V_T_inv = V_T_inv

            self.MEANS = means

    def set_errors(self, errors, reduce_to_selected_scales=False):
        """
        Set error data table

        :param errors: error data to set
        """
        if reduce_to_selected_scales:
            # create the filter for the data vector
            filter = self._create_filter()
            errors = errors[:, filter]
        self.ERRORS = errors

    def set_precision_matrices(self, inv_cov_matrices, apply_SVD=False,
                               reduce_to_selected_scales=False, inverted=False,
                               check_inversion=True):
        """
        Set precision matrices

        :param inv_cov_matrices: Precision/covariance matrices.
                                 If covariance matrices given they will be
                                 inverted. The shape should be (number of
                                 configurations, data vector length,
                                 data vector length)
        :param apply_SVD: Reduce dimensionality of data using SVD
        :param reduce_to_selected_scales: If True cuts out all scales from the
                                          multiscale datavector that are not
                                          in ctx[selected_scales].
                                          Based on the filter function in the
                                          statistic plugin.
        :param inverted: If True assumes that covariance matrices are
                         already inverted. If False inverts them and performs
                         numerical stability checks. Note: If already inverted
                         cannot use SVD.
        :param check_inversion: If True checks numerical stability of inversion
                                of the fiducial covariance matrix
        """
        if reduce_to_selected_scales:
            if inverted:
                raise Exception(
                    "You are attempting to slice inverted "
                    "covariance matrices. This is probably not what you want")
            # create the filter for the data vector
            filter = self._create_filter()

            # slice the covariance matrices
            new = np.zeros(
                (inv_cov_matrices.shape[0], np.sum(filter), np.sum(filter)))
            for ii in range(inv_cov_matrices.shape[0]):
                temp = inv_cov_matrices[ii, :, :]
                temp = temp[filter, :]
                temp = temp[:, filter]
                new[ii, :, :] = temp
            inv_cov_matrices = new

        if apply_SVD:
            if len(self.S_inv) == 0:
                raise Exception("SVD not build. Cannot transform to SVD basis")
            if inverted:
                raise Exception("Cannot apply SVD to inverted covariances.")
            s = np.linalg.inv(self.S_inv)
            vh = np.linalg.inv(self.V_T_inv)
            idx = self.SVD_selection

            temp = np.zeros((inv_cov_matrices.shape[0],
                             np.sum(idx), np.sum(idx)))
            for ii in range(inv_cov_matrices.shape[0]):
                C_ = np.dot(self.V_T_inv.T, np.dot(
                    inv_cov_matrices[ii, :, :], self.V_T_inv))
                idx_ = np.asarray(
                    [True] * s.shape[0] + [False] * (vh.shape[0] - s.shape[0]))
                C_ = C_[idx_, :]
                C_ = C_[:, idx_]
                C = np.dot(self.S_inv.T, np.dot(C_, self.S_inv))
                C = C[idx, :]
                C = C[:, idx]
                temp[ii, :, :] = C
            inv_cov_matrices = temp
        elif (not apply_SVD) & (len(self.S_inv) > 0):
            vprint(
                "SVD is built and you are resetting the precision matrices "
                "without applying the SVD transformation! Assuming the given "
                "matrices are in SVD basis already", logger=self.logger,
                verbose=True, level='warning')

        self.INCOVS = inv_cov_matrices
        if not inverted:
            vprint("Assuming that given matrices are not inverted, Inverting.",
                   verbose=self.verbose, logger=self.logger)
            self._invert_cov_matrices(check_inversion=check_inversion)

    def set_interpolator(self, interpolator):
        """
        Set interpolators manually

        :param interpolator: Interpolators to set
        """
        if len(self.S_inv) > 0:
            vprint(
                "You are resetting the interpolator with SVD already applied. "
                "The set interpolator is considered to act in the SVD basis. ",
                logger=self.logger, verbose=self.verbose, level='warning')
        self.interpolator = interpolator

    def set_precision_interpolator(self, interpolator):
        """
        Set interpolators for precision matrix manually

        :param interpolator: Interpolators to set
        """
        if len(self.S_inv) > 0:
            vprint(
                "You are resetting the interpolator with SVD already applied. "
                "The set interpolator is considered to act in the SVD basis. ",
                logger=self.logger, verbose=self.verbose, level='warning')
        self.cov_interpolator = interpolator

    def set_emulators(self, emulators):
        """
        Set emulators manually

        :param emulators: Table of polynomial coefficients to set
        """
        self.emulators = emulators

    def set_fiducial_precision_matrix(self, matrix):
        """
        If no interpolation of the precision matrix is used. The fiducial one
        is used everywhere. Can set it manually with this function.

        :param matrix: The central precision matrix to set
        """
        self.precision_matrix = matrix

    # METHODS

    def readin_interpolation_data(self, means_path, meta_path='', cov_path='',
                                  error_path='', inverted=False,
                                  reduce_to_selected_scales=False,
                                  use_SVD=False,
                                  systematics=True, check_inversion=True):
        """
        Loads data used for interpolation. The data is expected to be in a
        format as used by the estats.summary module

        :param means_path: Path to file holding mean datavectors for
                           each cosmology or the data array directly.
                           Shape: (realisations, length of data)
        :param cov_path: Path to file holding covariance or inverted
                         covariances for each cosmology or the data array
                         directly.
                         Shape: (realisations, length of data, length of data)
        :param meta_path: Path to file holding meta data table or the data
                          array directly. Shape: (realisations, number of meta
                          data entries)
        :param error_path: Path to file holding error vectors or the data
                           array directly. Shape: (realisations, length of
                           data)
        :param inverted: If True assumes that covariance matrices are
                         already inverted. If False inverts them and performs
                         numerical stability checks. Note: If already inverted
                         cannot use SVD.
        :param reduce_to_selected_scales: If True cuts out all scales from the
                                          multiscale datavector that are not
                                          in ctx[selected_scales].
                                          Based on the filter function in the
                                          statistic plugin.
        :param use_SVD: Reduce dimensionality of data using SVD
        :param systematics: If True capture variance in nuisance parameters
                            as well with the SVD.
        :param check_inversion: If True checks numerical stability of inversion
                                of the fiducial covariance matrix
        """

        vprint("Loading the mean data vectors for different \
               parameter configurations from {}".format(
            means_path), verbose=self.verbose, logger=self.logger)

        if len(meta_path) > 0:
            vprint("Loading the meta data for different \
                    parameter configurations from {}".format(
                meta_path), verbose=self.verbose, logger=self.logger)
            if isinstance(meta_path, str):
                META = np.load(meta_path)
            else:
                META = meta_path
        self.set_meta(META)

        if isinstance(means_path, str):
            MEANS = np.load(means_path)
        else:
            MEANS = means_path
        self.set_means(MEANS, systematics,
                       reduce_to_selected_scales, use_SVD)

        if len(cov_path) > 0:
            vprint("Loading the Covariance matrices for \
                    different parameter configurations from {}".format(
                cov_path), verbose=self.verbose, logger=self.logger)
            if isinstance(cov_path, str):
                COVS = np.load(cov_path)
            else:
                COVS = cov_path
            self.set_precision_matrices(
                COVS, apply_SVD=use_SVD,
                reduce_to_selected_scales=reduce_to_selected_scales,
                inverted=inverted, check_inversion=check_inversion)

        if len(error_path) > 0:
            if isinstance(error_path, str):
                ERRORS = np.load(error_path)
            else:
                ERRORS = error_path
            self.set_errors(ERRORS, reduce_to_selected_scales)

    def build_interpolator(self, interpolate_precision_matrix=False,
                           interp_border=[], selector=None, complexity=[3, 3]):
        """
        Build the interpolator for the parameters used to interpolate
        between different parameter setups.

        :param interpolate_precision_matrix: If True uses a parameter
                                             dependent precision matrix
                                             (interpolates it) otherwise uses
                                             the one at the fiducial parameter
                                             setup.
        :param interp_border: Only for method=multi. The limits of the
                              parameters up to where interpolator is working.
                              Format [min_1, max_1, min_2, max_2]
        :param selector: Can provide a boolean array to preselect the mean
                         datavectors to be considered for the construction of
                         the interpolator
        :param complexity: For multi mode, the complexity of the piecewise
                           smooth splines, along the two parameter directions.
        """
        vprint("Building Multidimensional interpolator function to "
               "interpolate data vecotrs to different cosmologies",
               verbose=self.verbose, logger=self.logger)

        # use only data realisations where nuisances are set to default
        params = {}
        for ii, param in enumerate(self.ctx['nuisances']):
            params[param] = self.ctx['nuisance_fiducials'][ii]
        chosen = self._get_loc(params, preselection=selector)

        # create the meta data for the interpolator
        meta = np.zeros((np.sum(chosen), 0))
        for param in self.ctx['parameters']:
            meta = np.hstack((meta, self.META[param][chosen].reshape(-1, 1)))

        if interpolate_precision_matrix:
            self.interpolate_precision_matrix = True
            # create interpolation data array
            data_length = self.INCOVS.shape[1]
            cov_interpolation_data = np.zeros(
                (np.sum(chosen), data_length * data_length))

            for it, ii in enumerate(np.where(chosen)[0]):
                cov_interpolation_data[it, :] = self.INCOVS[ii, :, :].ravel()
        else:
            self.interpolate_precision_matrix = False

        # create interpolation data array
        data_length = self.MEANS.shape[1]
        interpolation_data = np.zeros((np.sum(chosen), data_length))

        for it, ii in enumerate(np.where(chosen)[0]):
            interpolation_data[it, :] = self.MEANS[ii, :].reshape(1, -1)

        # set global precision matrix to
        # the one at the fiducial configuration
        params = {}
        for ii, param in enumerate(self.ctx['parameters']):
            params[param] = self.ctx['parameter_fiducials'][ii]
        fid_chosen = self._get_loc(params)
        fid_chosen = np.logical_and(fid_chosen, chosen)
        if np.sum(fid_chosen) != 1:
            raise Exception("Too many or no reference runs!")
        if (not interpolate_precision_matrix) & (len(self.INCOVS) > 0):
            self.precision_matrix = self.INCOVS[fid_chosen, :, :]
            self.INCOVS = []

        if self.ctx['method'] == 'linear':
            vprint("DEPRECATED", verbose=True, logger=self.logger,
                   level='warning')
            self.interpolator = LinearNDInterpolator(meta, interpolation_data)
        elif self.ctx['method'] == 'cubic':
            vprint("DEPRECATED", verbose=True, logger=self.logger,
                   level='warning')
            if len(self.ctx['parameters']) > 2:
                raise Exception(
                    "Cannot use cubic mode in more then "
                    "2 dimensions (use method = linear)")
            self.interpolator = CloughTocher2DInterpolator(
                meta, interpolation_data)
        elif self.ctx['method'] == 'multi':
            # interpolate each element of data vector separately
            if len(self.ctx['parameters']) > 2:
                raise Exception(
                    "Cannot use multi mode in more then "
                    "2 dimensions (use method = linear)")
            if interpolate_precision_matrix:
                self.cov_interpolator = []
                for i in range(cov_interpolation_data.shape[1]):
                    self.cov_interpolator.append(SmoothBivariateSpline(
                        meta[:, 0], meta[:, 1], cov_interpolation_data[:, i],
                        bbox=interp_border, kx=complexity[0],
                        ky=complexity[1]))

            self.interpolator = []
            for i in range(interpolation_data.shape[1]):
                self.interpolator.append(SmoothBivariateSpline(
                    meta[:, 0], meta[:, 1], interpolation_data[:, i],
                    bbox=interp_border, kx=complexity[0], ky=complexity[1]))
        vprint("Built cosmology interpolator",
               verbose=self.verbose, logger=self.logger)

    def build_emulator(self):
        """
        Builds the emulators for the nuisance parameters individually for each
        data bin (requires less dense sampling than full interpolator).
        There is a hardcoded emulator when using
        parameters as Om, s8 and nuisances IA, m, delta z. Otherwise fits a
        piecewise spline for each nuisance individually (assuming each nuisance
        parameter to be independent of the other ones and the parameters).
        """
        vprint("Building nuisance emulators",
               verbose=self.verbose, logger=self.logger)

        # use subset of parameter space to build defined with
        # selected_parameters
        chosen = [False] * self.META.shape[0]
        for s in range(len(self.ctx['selected_parameters'][0])):
            params = {}
            for ii, param in enumerate(self.ctx['parameters']):
                params[param] = self.ctx['selected_parameters'][ii][s]
            chosen = np.logical_or(chosen, self._get_loc(params))

        META = self.META[chosen]
        MEANS = self.MEANS[chosen, :]

        # use only data realisations where nuisances
        # are set to default for the reference run
        ref_chosen = [True] * META.shape[0]
        for ii, nuis in enumerate(self.ctx['nuisances']):
            idx = np.isclose(META[nuis], self.ctx['nuisance_fiducials'][ii])
            ref_chosen = np.logical_and(ref_chosen, idx)

        reference_runs = MEANS[ref_chosen, :]
        META_ref = META[ref_chosen]

        # convert meta to unstructured array
        META_ref = META_ref.view(np.float64).reshape(
            META_ref.shape + (-1,))[:, 2:]
        META = META.view(np.float64).reshape(META.shape + (-1,))[:, 2:]

        # calculate the ratio to the reference
        RATIOS = np.zeros_like(MEANS)
        for entry in range(MEANS.shape[0]):
            # get corresponding reference run
            ref_chosen = [True] * META_ref.shape[0]
            for ii, param in enumerate(self.ctx['parameters']):
                idx = np.isclose(META_ref[:, ii], META[entry, ii])
                ref_chosen = np.logical_and(ref_chosen, idx)
            RATIOS[entry] = (
                MEANS[entry, :] - reference_runs[ref_chosen, :]) \
                / reference_runs[ref_chosen, :]

        # fit emulators for each data vector bin
        self.emulators = []
        if np.array_equal(self.ctx['nuisances'], ['IA', 'm', 'z']) & \
           np.array_equal(self.ctx['parameters'], ['Om', 's8']):
            vprint("Found parameters to be Om, s8 and nuisances IA, m, "
                   "delta z. -> Fitting polynomial model hardcoded for this "
                   "case.", logger=self.logger, verbose=True, level='warning')
            for i in range(RATIOS.shape[1]):
                self.emulators.append(_fit_polynomial(META, RATIOS[:, i]))
        else:
            vprint("Generic Emulator case. Fitting piecewise ND spline"
                   "individually for each parameter bin", level='warning',
                   logger=self.logger, verbose=True)
            for i in range(RATIOS.shape[1]):
                self.emulators.append(
                    LinearNDInterpolator(
                        META[:, len(self.ctx['parameters']):], RATIOS[:, i]))

        vprint("Built nuisance emulators",
               verbose=self.verbose, logger=self.logger)

    def get_neg_loglikelihood(self, params, measurement, debias=False):
        """
        Returns negative loglikelihood given a measurement data vector at the
        location in parameter space indicated by params.

        :param params: List/Dictionary of the parameters where to calculate
                       the loglikelihood
        :param measurement: The measurement data vector to comapre to
        :param debias: If True use likelihood considering estimated precision
                       matrix and data vectors
        :return: Negative loglikelihood
        """

        params = self._convert_dict_list(params, t='list')

        # Get prior
        prior = self._get_prior(params)

        # If not outside of prior range rescale reference
        # data vector according to nuisance emulators
        if not np.isinf(prior):
            # prediction of datavector
            mean = self._get_interp_data_vector(params, len(self.S_inv) > 0)

            # Get interpolated precision matrix
            incov = self._get_interp_precision_matrix(params)

            measurement = measurement.reshape(-1, 1)

            # perform SVD on measurement
            if len(self.S_inv) > 0:
                measurement = self._single_SVD(measurement)

            # Calculate the likelihood
            Q = self._get_likelihood(measurement, mean, incov,
                                     debias=debias)
        else:
            Q = 0.0

        # get neg loglike
        log_like = -0.5 * (Q + prior)

        if np.isnan(log_like):
            return -np.inf
        if not np.isfinite(log_like):
            return -np.inf

        return log_like

    # HELPER FUNCTIONS

    def _scale_peak_func(self, params):
        """
        Get scale factors from emulator which one needs to multiply to
        the datavector
        in order to emulate a certain nuisance configuration
        """

        scale = np.ones(self.MEANS.shape[1])

        # decide to use default or the polynomial model
        if np.array_equal(self.ctx['nuisances'], ['IA', 'm', 'z']) & \
           np.array_equal(self.ctx['parameters'], ['Om', 's8']):
            if len(params) != (2 + 1 + self.ctx['n_tomo_bins'] * 2):
                raise Exception("When using the polynomial model Need one "
                                "nuisance for IA and number of "
                                "tomographic bins for m and z!")
            for s in range(scale.size):
                # IA
                nuis = [params[2]]

                # in case of tomography and cross spectra use mean of the
                # two nuisances for the crosses
                bin = self.bin_array[s]
                if 'x' in bin:
                    # assume binxbin entry
                    b = [int(bin.split('x')[0]) - 1,
                         int(bin.split('x')[1]) - 1]
                else:
                    b = [int(bin), int(bin)]
                # m
                nuis.append(np.mean([params[3 + b[0]], params[3 + b[1]]]))
                # delta z
                nuis.append(
                    np.mean([params[3 + self.ctx['n_tomo_bins'] + b[0]],
                             params[3 + self.ctx['n_tomo_bins'] + b[1]]]))

                scale[s] += _weight_func(
                    np.append(params[:2], nuis), self.emulators[s])
        else:
            for s in range(scale.size):
                scale[s] += self.emulators[s](
                    *params[len(self.ctx['parameters']):])

        return scale

    def _get_likelihood(self, meas, mean, incov, debias=False):
        """
        Returns likelihood using either standard Gaussian likelihood or using
        debiasing due to estimated cov marix and predicted datavaectors
        (debias=True)
        """
        diff = mean - meas
        Q = np.dot(diff.reshape(1, -1), np.dot(incov, diff)).reshape(1)[0]
        if debias:
            """
            According to:
            Jeffrey, Niall, and Filipe B. Abdalla. Parameter inference and
            model comparison using theoretical predictions from noisy
            simulations. Monthly Notices of the Royal Astronomical
            Society 490.4 (2019): 5749-5756.
            """

            params = {}
            for ii, param in enumerate(self.ctx['parameters']):
                params[param] = self.ctx['parameter_fiducials'][ii]
            for ii, param in enumerate(self.ctx['nuisances']):
                params[param] = self.ctx['nuisance_fiducials'][ii]
            chosen = self._get_loc(params)
            N_cov = self.META[chosen]['NREALS']
            N_mean = np.mean(self.META['NREALS'])

            Q = 1. + Q * N_mean / ((N_mean + 1.) * (N_cov - 1.))
            Q *= N_cov

        return Q

    def _get_prior(self, params):
        """
        Prior function
        """
        prior = 0.0
        for ii in range(len(params)):
            prior_config = self.ctx['prior_configuration'][ii]
            if prior_config[0] == 'flat':
                if params[ii] < prior_config[1]:
                    prior += np.inf
                if params[ii] > prior_config[2]:
                    prior += np.inf
            elif prior_config[0] == 'normal':
                prior += ((params[ii] - prior_config[1]) / prior_config[2])**2.
        return prior

    def _create_filter(self):
        """
        Creates a filter that cuts out the required data vector elements
        and an array indicating the tomographic bins for the emulator
        """

        def get_tomo_bin_num(stat, ctx):
            if 'Cross' in stat:
                tomo_bins = int(scipy.special.binom(
                    ctx['n_tomo_bins'] + 2 - 1,
                    ctx['n_tomo_bins'] - 1))
                if tomo_bins == 1:
                    # skip for non tomographic case + cross spectra
                    tomo_bins = 0
            else:
                tomo_bins = self.ctx['n_tomo_bins']
            return tomo_bins

        filter = np.zeros(0, dtype=bool)
        bin_filter = np.zeros(0, dtype=str)

        stats = self.ctx['statistic'].split('-')

        for stat in stats:
            plugin = utils.import_executable(stat, 'filter',
                                             self.verbose, self.logger)
            # determine number of different tomographic bins
            tomo_bins = get_tomo_bin_num(stat, self.ctx)
            for bin in range(tomo_bins):
                f = plugin(self.ctx)
                filter = np.append(filter, f)
                if 'Cross' in stat:
                    bin_val = self.ctx['cross_ordering'][bin]
                else:
                    bin_val = bin
                bin_filter = np.append(
                    bin_filter, [bin_val] * int(np.sum(f)))
        self.bin_array = bin_filter
        return filter.astype(bool)

    def _get_loc(self, params, exclude=False, preselection=None):
        """
        Get a filter for data realisations where parameters are set to params
        """
        if preselection is None:
            chosen = [True] * self.META.shape[0]
        else:
            chosen = preselection
        for param in params.keys():
            idx = np.isclose(self.META[param], params[param])
            chosen = np.logical_and(chosen, idx)
        if exclude:
            chosen = np.logical_not(chosen)
        return chosen

    def _get_interp_data_vector(self, params, use_SVD):
        """
        Returns an interpolated data vector at parameters params
        """

        # Get interpolated precision matrix and data vector at the cosmology
        if self.ctx['method'] == 'multi':
            mean = []
            for interpol in self.interpolator:
                mean.append(
                    interpol(*params[:len(self.ctx['parameters'])]).ravel())
            mean = np.asarray(mean)
        else:
            mean = self.interpolator(params[:len(self.ctx['parameters'])])

        mean = mean.reshape(-1, 1)

        # scaling with emulator
        if len(params) > len(self.ctx['parameters']):
            if len(self.emulators) > 0:
                scale_facs = self._scale_peak_func(params).reshape(-1, 1)
                mean = mean * scale_facs
            else:
                vprint("Found nuisance parameters but emulator was not built, "
                       "Ignoring...", verbose=True, logger=self.logger,
                       level='warning')

        # perform SVD on prediction
        if use_SVD:
            mean = self._single_SVD(mean)
        return mean

    def _invert_cov_matrices(self, check_inversion=True):
        """
        Inverts covariance matrices
        """
        # only print condition number for fiducial setup
        params = {}
        for ii, param in enumerate(self.ctx['parameters']):
            params[param] = self.ctx['parameter_fiducials'][ii]
        for ii, param in enumerate(self.ctx['nuisances']):
            params[param] = self.ctx['nuisance_fiducials'][ii]
        chosen = np.where(self._get_loc(params))[0]

        temps = []
        if len(self.INCOVS) > 0:
            for ii in range(self.INCOVS.shape[0]):
                # compute condition numbers with different norms
                if (ii == chosen) & (check_inversion):
                    vprint(
                        '================================================',
                        logger=self.logger, verbose=self.verbose)
                    vprint(
                        "Mean of datavectors: {}".format(
                            np.mean(self.MEANS)),
                        logger=self.logger, verbose=self.verbose)
                    norms = [None, 'fro', np.inf, -np.inf, 1, -1, 2, -2]
                    for norm in norms:
                        cond_num = np.linalg.cond(self.INCOVS[ii, :, :],
                                                  p=norm)
                        vprint(
                            "For norm {} the condition number is "
                            "{}".format(norm, cond_num),
                            logger=self.logger, verbose=self.verbose)
                    vprint(
                        '================================================',
                        logger=self.logger, verbose=self.verbose)

                    # checking stability of inversion
                    id_check = np.dot(self.INCOVS[ii, :, :],
                                      np.linalg.inv(self.INCOVS[ii, :, :]))
                    id = np.eye(id_check.shape[0])
                    if not np.allclose(id_check, id):
                        raise Exception(
                            "Inversion of Fiducial Covariance matrix "
                            "did not pass numerical stability test")
                    else:
                        vprint("Successfully inverted Fiducial "
                               "Covariance matrix",
                               logger=self.logger, verbose=self.verbose)

                temps.append(np.linalg.inv(self.INCOVS[ii, :, :]))
        self.INCOVS = np.asarray(temps)

    def _get_interp_precision_matrix(self, params):
        """
        Return inerpolated covariance matrix at params
        """
        if self.interpolate_precision_matrix:
            interp = []
            for ii in range(len(self.cov_interpolator)):
                interp.append(
                    self.cov_interpolator[ii](
                        *params[:len(self.ctx['parameters'])]))
            incov = np.asarray(interp).reshape(self.INCOVS.shape[1],
                                               self.INCOVS.shape[1])
        else:
            incov = self.precision_matrix
        return incov

    def _single_SVD(self, vec):
        """
        Perform SVD on single datavector
        """
        vec = np.dot(vec.T, self.V_T_inv)
        idx_ = np.asarray(
            [True] * self.S_inv.shape[0]
            + [False] * (self.V_T_inv.shape[0] - self.S_inv.shape[0]))
        vec = vec.T[idx_]
        vec = np.dot(vec.T, self.S_inv)
        vec = vec.T[self.SVD_selection]
        return vec

    def _convert_dict_list(self, obj, t='list'):
        """
        Converts dictionary to list or the othwer way round
        """
        if isinstance(obj, dict):
            f = 'dict'
        elif (isinstance(obj, list)) | (isinstance(obj, np.ndarray)):
            f = 'list'
        else:
            raise Exception("{} is not a list nor a dictionary".format(obj))

        if f == t:
            return obj
        elif (f == 'dict') & (t == 'list'):
            list_ = []
            for key in self.ctx['parameters']:
                if key in list(obj.keys()):
                    list_.append(obj[key])
            for key in self.ctx['nuisances']:
                if key in list(obj.keys()):
                    list_.append(obj[key])
            return list_

        elif (f == 'list') & (t == 'dict'):
            if len(list(obj.keys())) == len(self.ctx['parameters']):
                vprint(
                    "The length of the oject {} matches only the number of "
                    "parameters. Assuming that only parameters and no "
                    "nuisances given.".format(obj), logger=self.logger,
                    verbose=self.verbose)
                check = False
            elif len(list(obj.keys())) == \
                    (len(self.ctx['parameters']) + len(self.ctx['nuisances'])):
                check = True
            else:
                raise Exception(
                    "The list {} does not contain the right number of "
                    "parameters. Either only parameters or parameters + "
                    "nuisances".format(obj))

            dict_ = {}
            for ik, key in enumerate(self.ctx['parameters']):
                dict_[key] = obj[ik]
            if check:
                for key in self.ctx['nuisances']:
                    if key in list(obj.keys()):
                        list.append(obj[key])
            return dict_


def _fit_polynomial(grid, values):
    """
    Fits a polynomial series to data. Assumes 2 cosmological and 3
    systematic parameters in order Omegam, sigma8, IA, m, deltaz.

    :param grid: 2D array containing the data points for fitting.
                 Shape is (...), 5)
    :param values: Array of values to fit to
    :return: The fitted polynomial coefficients
    """

    OM = grid[:, 0]
    S8 = grid[:, 1]
    IA = grid[:, 2]
    M = grid[:, 3]
    Z = grid[:, 4]

    OM = OM.flatten()
    S8 = S8.flatten()
    IA = IA.flatten()
    M = M.flatten()
    Z = Z.flatten()

    # Pure Nuis terms
    A_NUIS = [IA, IA**2., M, M**2., Z, Z**2.]
    # Nuis-Cos terms
    A_NUIS_COS = [IA * OM * S8, IA * S8, IA**2. * OM, IA**2. * S8,
                  M * OM, M * S8, Z * OM, Z * S8]
    # Nuis-Cross terms
    A_NUIS_CROSS = [IA * M, M * Z, IA * Z]

    A = np.array(A_NUIS + A_NUIS_COS + A_NUIS_CROSS).T

    B = values.flatten()
    W = np.ones_like(B)

    # WLS
    Xw = A * np.sqrt(W)[:, None]
    yw = B * np.sqrt(W)
    yw[np.isnan(B)] = 0.0
    coeff, r, rank, s = scipy.linalg.lstsq(Xw, yw)
    return coeff


def _weight_func(grid, coeff=[]):
    """
    Evaluates the polynomial defined by the coeffs at points in grid.

    :param grid: 2D array containing the data points for fitting.
                 Shape is(..., 5)
    :param coeff: Array of polynomial coefficients
    :return: The scale factor at the different grid points
    """

    OM = grid[0]
    S8 = grid[1]
    IA = grid[2]
    M = grid[3]
    Z = grid[4]

    # Pure Nuis terms
    A_NUIS = [IA, IA**2., M, M**2., Z, Z**2.]
    # Nuis-Cos terms
    A_NUIS_COS = [IA * OM * S8, IA * S8, IA**2. * OM, IA**2. * S8,
                  M * OM, M * S8, Z * OM, Z * S8]
    # Nuis-Cross terms
    A_NUIS_CROSS = [IA * M, M * Z, IA * Z]

    poly_grid = np.array(
        A_NUIS + A_NUIS_COS + A_NUIS_CROSS)

    result = 0.0
    for ii in range(poly_grid.shape[0]):
        result += coeff[ii] * poly_grid[ii]
    return result
