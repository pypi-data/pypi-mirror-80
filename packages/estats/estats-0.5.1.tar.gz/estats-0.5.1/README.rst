===========================
estats Version 0.4.1 - BETA
===========================

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/estats/badges/master/coverage.svg
  		:target: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/estats

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/estats/badges/master/pipeline.svg
        :target: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/estats

.. image:: http://img.shields.io/badge/arXiv-2006.12506-orange.svg?style=flat
        :target: https://arxiv.org/abs/2006.12506


This package is part of the Non-Gaussian Statistics Framework (`NGSF <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/NGSF>`_).

If you use this package in your research please cite Zuercher et al. 2020. (`arXiv-2006.12506 <https://arxiv.org/abs/2006.12506>`_).


`Source <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/estats>`_

`Documentation <http://cosmo-docs.phys.ethz.ch/estats>`_


Introduction
============

The estats package contains the main building blocks of the NGSF.
It was initially built to constrain cosmological parameters using Non-Gaussian
statistics on weak lensing mass maps.
The different submodules are independent of each other and can easily
be used in other codes individually.

catalog
-------

The catalog module handles a galaxy catalog consisting out of
coordinates, ellipticities, weights and tomographic bins for each galaxy.
Main functionalities: Can rotate the catalog on the sky, output
survey mask, weight map, shear and convergence maps.
Also allows generation of noise catalogs / shear maps using random
rotation of the galaxies in place.

The most important functionalities are:

- rotate_catalog:

    Allows to rotate the survey on the sky by given angles.

- get_mask:

    Returns the survey mask as a Healpix
    (`Gorski et al. 2005 <https://iopscience.iop.org/article/10.1086/427976>`_)
    map.

- get_map:

    Can return Healpix
    shear maps, convergence maps or a weight map
    (number of galaxies per pixel). The convergence map is calculated from
    the ellipticities of the galaxies using the spherical Kaiser-Squires
    routine (`Wallis et al. 2017 <https://arxiv.org/pdf/1703.09233.pdf>`_).
    The shear and convergence maps are properly weighted.

- generate_shape_noise_map:

    Generates a shape noise Healpix shear map by random rotation of the galaxies
    ellipticities in place.
    The weights are considered when generating the noise map.

map
---

The map module handles shear and convergence maps and calculate summary statistics from them.
One instance can hold up to two sets of weak lensing maps. Each set
is constituted out of a survey mask, a trimmed survey mask (tighter survey mask
meant to be used to disregard pixels at the edge of the mask, where large errors
are introduced due to the spherical harmonics transformation), 2 convergence maps (E and B modes),
a weight map and 2 shear maps (first and second component).

The summary statistics are defined via plugins that are located in the estats.stats folder.
This allows users to easily add their own summary statistic without having to
modify the internals of the code.
See the "Implementing your own summary statistics" Section to learn how to do that.

The summary statistics can be calculated from the shear maps, the convergence maps
or from a smoothed convergence maps (multiscale approach for extraction of non-Gaussian features).

If only one set of weak lensing maps is given the statistics will be calculated from that set
directly. If two sets are given and the name of the statistic to be computed contains the word Cross
both sets are passed to the statistics plugin. This can be used to calculate cross-correlations
between maps from different tomographic bins for example.

The most important functionalities are:

- convert_convergence_to_shear:

    Uses spherical Kaiser-Squires to convert the internal shear maps to
    convergence maps. The maps are masked using the internal masks.
    By default the trimmed mask is used to allow the user to disregard
    pixels where the spherical harmonics transformation introduced large errors.

- convert_shear_to_convergence:

    Uses spherical Kaiser-Squires to convert the internal E-mode convergence map to
    shear maps. The maps are masked using the internal masks.
    By default the trimmed mask is used to allow the user to disregard
    pixels where the spherical harmonics transformation introduced large errors.

- smooth_maps:

    Applies a Gaussian smoothing kernel to all internal convergence maps
    (E- and B-modes). The fwhm parameter decides on the FWHM of the Gaussian
    smoothing kernel. It is given in arcmin.

- calc_summary_stats:

    Main functionality of the module. Allows to use statistics plugins located in
    the estats.stats folder to calculate map based statistics.

    See the "Implementing your own summary statistics" Section to learn how the statistics plugins look
    like and how to make your own one.

    The summary statistics can be calculated from the shear maps, the convergence maps
    or from a smoothed convergence maps (multiscale approach for extraction of non-Gaussian features).

    If only one set of weak lensing maps is given the statistics will be calculated from that set
    directly. If two sets are given and the name of the statistic to be computed contains the word Cross
    both sets are passed to the statistics plugin. This can be used to calculate cross-correlations
    between maps from different tomographic bins for example.

    Instead of using the internal masks for masking, extra masks can be used.
    This allows to use maps with multiple survey cutouts on it and select a
    different cutout each time the function is called.

    If use_shear_maps is set to True the function will convert the shear maps
    into convergence maps using spherical Kaiser-Squires instead of using the convergence maps directly.

    If copy_obj is set to False, no copies of the internal maps are made.
    This can save RAM but it also leads to the internal maps being overwritten.
    If you wish to use the internal maps after the function call set this to
    True!

    By default the function returns the calculated statistics in a dictionary.
    But if write_to_file is set to True it will append to files that are defined
    using the defined_parameters, undefined_parameters, output_dir and name arguments using ekit.paths.

    Note: If the CrossCLs statistic is used without secondary maps set the
    convergence and weights maps will be written onto a Healpix map.
    The path to the map is defined over the defined_parameters, undefined_parameters,
    output_dir and name arguments using ekit.paths.

summary
-------

The summary module is meant to postprocess summary statistics measurements.

The main functionality of the summary module is to calculate mean data-vectors,
standard deviations and covariance or precision matrices for the summary statistics
at different parameter configurations, based on a set of realizations of the
summary statistic at each configuration.

The meta data (e.g. cosmology setting, precision settings, tomographic bin and so on)
for each set of realizations (read-in from a file or an array directly) can be
given to the module on read-in directly or parsed from the filename.
Directly after read-in a first postprocessing can be done using the process
function defined in the statistic plugin.
The read-in data-vectors are stored appended to a data table for each statistic and the
meta data is added to an internal meta data table.
The realizations are ordered according to their meta data entry. There are two
special entries for the meta data (tomo: label for the tomographic bin of the
data-vectors, NREALS: the number of data-vectors associated to each entry (is inferred automatically)).
All other entries can be defined by the user.

The summary module allows to downbin the potentially very long data-vectors
into larger bins using a binning scheme.
The decide_binning_scheme function in the statistic plugin is used to decide on
that scheme, which defines the edges of the large bins based on the bins
of the original data-vectors. For plotting purposes the binning scheme can also
define the values of each data bin (for example its signal-to-noise ratio).
The slice function in the statistic plugin then defines how exactly the binning
scheme is used to downbin each data-vector.
See the "Implementing your own summary statistics" Section for more details.

The summary module allows to combine summary statistics calculated for
different tomographic bins
to perform a tomographic analysis. The tomo entry in the meta data table
defines the label of the tomographic bin for each set of data-vector realizations.
One can define the order of the labels when combined into a joint data-vector
using the cross_ordering keyword.

The summary module also allows to combine different summary
statistics into a joint data-vector.

The most important functionalities are:

- generate_binning_scheme:

    Uses the decide_binning_scheme function from the statistic plugin to
    create a binning scheme. The scheme can be created for different tomographic
    bins and scales. See the Section "Implementing your own summary statistics" for more details.

- readin_stat_files:

    Reads in data-vector realizations from a file. The process function from the statistics
    plugin is used to perform a first processing of the data. The meta data for each
    file can either be given directly or can be parsed from the file name by giving a
    list of parameters indicating the fields to be parsed (using ekit).

- downbin_data:

    Uses the created binning scheme to bin the data-vector entries into larger bins.
    Uses the slice function from the statistics plugin to do so.

- join_redshift_bins:

    Joins all data-vector realizations of a specific statistic at the same configuration.
    The tomo entry in the meta data table
    defines the label of the tomographic bin for each set of data-vector realizations.
    One can define the order of the labels when combined into a joint data-vector
    using the cross_ordering keyword. If for a specific parameter configuration
    different number of realizations are found for different tomographic bins,
    only the minimum number of realizations is used to calculate the combined data-vectors.

- join_statistics:

    Creates a new statistic entry including the data table and the meta data table,
    by concatenating the data-vectors of a set of statistics. The new statistic
    has the name statistic1-statistic2-...
    If for a specific parameter configuration
    different number of realizations are found for different statistics,
    only the minimum number of realizations is used to calculate the combined data-vectors.

- get_means:

    Returns the mean data vectors of a statistic for the different configurations.

- get_meta:

    Returns the full meta data table for a statistic.

- get_errors:

    Returns the standard deviation of the data vectors of a statistic for the different configurations.

- get_covariance_matrices:

    Returns the covariance matrices estimated from the realizations at each configuration.
    Can also invert the covariance matrices directly to obtain the precision matrices.

likelihood
----------

Class meant to perform parameter inference based on predictions
of the data-vectors and covariance matrices at different parameter configurations.

The main functionality is calculate the negative logarithmic likelihood at a
given parameter configuration given a measurement data-vector.

The parameter space is broken down into two parts called parameters and nuisances,
that are treated differently.

To obtain the data-vector and precision matrix predictions at the different parameter
configurations a full interpolation is used. This requires a
sufficiently dense sampling of the parameter space.

The nuisance parameter space is treated as an extension and an emulator is built
for this part of the configuration space. Therefore, the part of the configuration
space that is associated to the nuisance parameters requires less dense sampling.
The nuisance space can be explored only at a few points in the parameter space.
There is a hard-coded emulator when using the parameters as Om, s8 and nuisances IA, m, z.
This emulator is described in Zuercher et al. 2020. (`arXiv-2006.12506 <https://arxiv.org/abs/2006.12506>`_).
Otherwise, a piecewise spline for each nuisance parameter is fit individually.
Note that this assumes that each nuisance parameter is sufficiently independent
of the other nuisance parameters and also the parameters. The user needs to
confirm this for herself/himself for her/his setup.

On read-in of the data used to build the interpolator and emulator the given
covariance matrices are inverted to obtain the precision matrices. This inversion
can be numerically unstable for very large matrices or ill behaved entries.
Therefore, one can use the filter function defined in the statistic plugin to
decide which data bins to use exactly in the inference or to leave out
scales when using a multiscale data-vector for example.
Additionally, a Singular-Value-Decomposition can be used to further reduce
the length of the data-vectors and the dimensionality of the matrices.

The most important functionalities are:

- readin_interpolation_data:

    Loads data used for interpolation. The data is expected to be in a
    format as used by the estats.summary module. Can apply the filter function
    and/or the Singular-Value-Decomposition.

- build_interpolator:

    Builds the interpolator for the parameter space used to interpolate
    the expected data-vectors and precision matrices between different
    parameter configurations. There are three different choices
    for the type of interpolator used at the moment.

- build_emulator:

    Builds the emulators for the nuisance parameters individually for each
    data bin (requires less dense sampling than using a full interpolator).
    There is a hard-coded emulator when using the parameters as Om, s8 and nuisances IA, m, z.
    This emulator is described in Zuercher et al. 2020. (`arXiv-2006.12506 <https://arxiv.org/abs/2006.12506>`_).
    Otherwise, a piecewise spline for each nuisance parameter is fit individually.
    Note that this assumes that each nuisance parameter is sufficiently independent
    of the other nuisance parameters and also the parameters.

- get_neg_loglikelihood:

    Returns negative logarithmic likelihood given a measurement data-vector at the
    location in parameter space indicated.

Getting Started
===============

The easiest and fastest way to learn about estats is to have a look at the Tutorial Section.

Credits
=======

This package was created by Dominik Zuercher (PhD student at ETH Zurich in Alexandre Refregiers `Comsology Research Group <https://cosmology.ethz.ch/>`_)

The package is maintained by Dominik Zuercher dominik.zuercher@phys.ethz.ch.

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
