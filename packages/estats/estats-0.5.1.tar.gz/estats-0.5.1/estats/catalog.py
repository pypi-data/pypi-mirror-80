# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp

from ekit import context
from ekit.logger import vprint
from estats import utils


class catalog:
    """
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
        (`Gorski et al. 2005
        <https://iopscience.iop.org/article/10.1086/427976>`_)
        map.

    - get_map:

        Can return Healpix
        shear maps, convergence maps or a weight map
        (number of galaxies per pixel). The convergence map is calculated from
        the ellipticities of the galaxies using the spherical Kaiser-Squires
        routine (`Wallis et al. 2017 <https://arxiv.org/pdf/1703.09233.pdf>`_).
        The shear and convergence maps are properly weighted.

    - generate_shape_noise_map:

        Generates a shape noise Healpix shear map by random rotation of the
        galaxies ellipticities in place. The weights are considered in the
        generation of the noise.

    The accepted keywords are:

    - NSIDE:

        default: 1024

        choices: an integer being a power of 2

        The Healpix resolution that is used to produce the map products.

    - degree:

        default: True

        choices: True, False

        If True the coordinates are assumed to be given in degrees otherwise
        in radians.

    - colat:

        default: False

        choices: True, False

        If True the second coordinate is assumed to be a co-latitude otherwise
        a normal latitude is assumed.

    - prec:

        default: 32

        choices: 64, 32, 16

        Size of the float values in the Healpix maps in bits. For less then 32
        hp.UNSEEN is mapped to -inf -> No RAM optimization anymore
    """

    def __init__(self, alphas=[], deltas=[], gamma_1s=[], gamma_2s=[],
                 redshift_bins=[], weights=[], context_in={}, store_pix=False,
                 logger=None, verbose=False, **kwargs):
        """
        Initialization function for catalog class.

        :param alphas: List of first coordinates, either in radians or degrees
        :param deltas: List of second coordinates, either in radians or degrees
        :param gamma_1s: List of first shear components
        :param gamma_2s: List of second shear components
        :param redshift_bins: List of integers indicating the redshift bin the
                              objects belong to (should start from 1 upwards)
        :param weights: List of object weights
        :param store_pix: If true only pixel location of objects is stored
                          (saves RAM but looses precision)
        :param context_in: A dictionary containing parameters.
        :param logger: A logger instance.
        :param verbose: Triggers verbose mode
        """

        self.verbose = verbose
        self.logger = logger

        vprint("Initializing catalog object", self.logger, self.verbose)

        # setup context
        allowed = ['NSIDE', 'degree', 'colat', 'prec']
        types = ['int', 'bool', 'bool', 'int']
        defaults = [1024, True, False, 32]

        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            logger=self.logger, verbose=self.verbose)

        self.ctx['prec'] = 'float{}'.format(self.ctx['prec'])

        # assign objects
        self.pixels = {}
        self.set_coordinates(alphas, deltas)
        self.set_ellipticities(gamma_1s, gamma_2s)
        self.set_weights(weights)
        self.set_redhift_bins(redshift_bins)
        if store_pix:
            self.pixels[0] = self._pixelize(alphas, deltas)
            self.alpha = []
            self.delta = []
            self.store_pix = True
        else:
            self.store_pix = False

        self._assert_lengths()

    # ACCESING OBJECTS

    def get_coordinates(self, bin=0):
        """
        Returns the coordinates of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        if len(self.alpha) > 0:
            return self.alpha[idx], self.delta[idx]
        else:
            delta, alpha = hp.pixelfunc.pix2ang(self.ctx['NSIDE'],
                                                self.pixels[0][idx])
            if self.ctx['degree']:
                alpha = np.degrees(alpha)
                delta = np.degrees(delta)
            if not self.ctx['colat']:
                delta = 90. - delta
            return alpha, delta

    def get_ellipticities(self, bin=0):
        """
        Returns the ellipticities of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        return self.gamma_1[idx], self.gamma_2[idx]

    def get_redshift_bins(self, bin=0):
        """
        Returns the redshift bins of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        bin = int(bin)
        idx = self._get_redshift_bool(bin)
        return self.redshift_bin[idx]

    def get_weights(self, bin=0):
        """
        Returns the weights of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        bin = int(bin)
        idx = self._get_redshift_bool(bin)
        return self.weights[idx]

    def get_pixels(self, pix_key=0, bin=0):
        """
        Returns the shears of the catalog objects

        :param pix_key: The key for the pixel dictionary
        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        if (len(self.pixels.keys()) == 0) & (pix_key == 0):
            pixs = self._pixelize(self.alpha, self.delta, bin=bin)
            return pixs[idx]
        else:
            return self.pixels[pix_key][idx]

    # CLEARING OBJECTS
    def clear_coordinates(self):
        """
        Clears arrays for coordinates
        """
        self.alpha = []
        self.delta = []

    def clear_ellipticities(self):
        """
        Clears arrays for ellipticities
        """
        self.gamma_1 = []
        self.gamma_2 = []

    def clear_redshift_bins(self):
        """
        Clears arrays for redshift bins
        """
        self.redshift_bin = []

    def clear_pixels(self):
        """
        Clears arrays for pixels
        """
        self.pixels = {}

    def clear_weights(self):
        """
        Clears arrays for weights
        """
        self.weights = []

    # SETTING OBJECTS
    def set_coordinates(self, alphas, deltas):
        """
        Sets coordinate arrays

        :param alphas: First coordinates
        :param deltas: Second coordinates
        """
        if (len(alphas) == 0) | (len(deltas) == 0):
            raise Exception(
                "Cannot set coordinates alpha and delta to empty arrays")
        self.alpha = alphas
        self.delta = deltas

    def set_ellipticities(self, gamma_1, gamma_2):
        """
        Sets elliticity arrays

        :param gamma_1: First  ellipticity component
        :param gamma_2: Second ellipticity component
        """
        if len(self.alpha) == 0:
            raise Exception(
                "Cannot set ellipticities if coordinates are not set")

        if (len(gamma_1) == 0) | (len(gamma_2) == 0):
            self.gamma_1 = np.zeros_like(self.alpha)
            self.gamma_2 = np.zeros_like(self.alpha)
        else:
            self.gamma_1 = gamma_1
            self.gamma_2 = gamma_2

    def set_redhift_bins(self, redshift_bins):
        """
        Sets redshift bin array

        :param redshift_bins: Redshift bins for the stored objects.
                              If empty set to 0
        """
        if len(self.alpha) == 0:
            raise Exception(
                "Cannot set ellipticities if coordinates are not set")

        if len(redshift_bins) == 0:
            self.redshift_bin = np.zeros_like(self.alpha, dtype=int)
        else:
            self.redshift_bin = redshift_bins

    def set_weights(self, weights):
        """
        Sets weight array

        :param weights: weights for the stored objects. If empty set to 1.
        """
        if len(self.alpha) == 0:
            raise Exception(
                "Cannot set ellipticities if coordinates are not set")

        if len(weights) == 0:
            self.weights = np.ones_like(self.alpha, dtype=int)
        else:
            self.weights = weights

    # METHODS
    def clip_shear_mag(self, clip_value):
        """
        Clips ellipticities at a provided value. Prevents extreme events.

        :param clip_value: The maximum absolute values
                           of the ellipticities that is allowed
        """
        # clipping
        clip_value = float(clip_value)
        gamma_mag = np.sqrt(self.gamma_1**2. + self.gamma_2**2.)
        flagged = np.where(gamma_mag > clip_value)[0]

        # remove flagged elements
        self.gamma_1 = np.delete(self.gamma_1, flagged)
        self.gamma_2 = np.delete(self.gamma_2, flagged)
        if len(self.alpha) > 0:
            self.alpha = np.delete(self.alpha, flagged)
            self.delta = np.delete(self.delta, flagged)
        for k in self.pixels.keys():
            self.pixels[k] = np.delete(self.pixels[k], flagged)
        self.redshift_bin = np.delete(self.redshift_bin, flagged)
        self.weights = np.delete(self.weights, flagged)

        self._assert_lengths()

    def rotate_catalog(self, alpha_rot, delta_rot, store_pixels=False,
                       mirror=False):
        """
        Rotates the galaxy coordinates on the sky. Can overwrite coordinates
        or just store the pixel coordinates of the rotated survey.

        :param alpha_rot: The angle along the first coordinates
                          to rotate (in rad)
        :param delta_rot: The angle along the second coordinates
                          to rotate (in rad)
        :param store_pixels: If False the old coordinates are overwritten.
                             If True old coordinates are conserved and only the
                             pixel numbers of the rotated objects are stored in
                             self.pixels. Allows holding many rotated catalogs
                             without requiring too much memory.
        :param mirror: If True mirrors all coordinates on the equator
        """

        alpha, delta = self._rotate_coordinates(
            alpha_rot, delta_rot, mirror)
        if store_pixels:
            pixs = self._pixelize(alpha, delta, bin=0, full_output=False)
            key = len(self.pixels.keys())
            self.pixels[key] = pixs
            vprint("The pixel locations of the rotated catalog have been "
                   "stored but the coordinates were rotated back",
                   self.logger, self.verbose)
        else:
            self.alpha, self.delta = alpha, delta
        self._assert_lengths()

    def get_object_pixels(self, bin=0, alpha_rot=0.0, delta_rot=0.0, pix=-1,
                          mirror=False):
        """
        Returns the pixel number of each object, all healpix pixels where the
        objects are located, the object indices and the object count in each
        pixel. Can optionally rotate the catalog.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
                    instead of the actual coordinates(-1 not used, greater or
                    equal than 0 indicates the map to use)
        :param mirror: If True mirrors coordinates on equator
        :return: Four lists containing the different pixelization information
        """
        # pixelize the coordinates
        if pix < -0.5:
            if len(self.alpha) == 0:
                vprint("Cannot create maps without coordinates",
                       verbose=self.verbose, logger=self.logger)
                return [], [], []

            # rotate catalog if appicable
            if (not np.isclose(alpha_rot, 0.0)) | \
               (not np.isclose(delta_rot, 0.0)) | \
               (mirror):
                alpha, delta = self._rotate_coordinates(
                    alpha_rot, delta_rot, mirror)
            else:
                alpha = self.alpha
                delta = self.delta
            unis, indices, pixs = self._pixelize(
                alpha, delta, bin, full_output=True)
        else:
            pixs = self.pixels[pix]
            unis, indices = np.unique(
                pixs, return_inverse=True)

        return (pixs, unis, indices)

    def get_map(self, type, bin=0, alpha_rot=0.0, delta_rot=0.0,
                pix=-1, trimming=True, mirror=False, normalize=True):
        """
        Creates weight, shear and convergence maps from the catalog.
        Can optionally rotate the catalog before.

        :param type: Can be weights, shear, convergence or a concatination of
                     them with '-'. Indicates type of maps returned.
        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
                    instead of the actual coordinates(-1 not used, greater or
                    equal than 0 indicates the map to use)
        :param trimming: If True applies stricter masking to convergence map
                         (some values on edges of survey mask can be
                         very off due to spherical harmonics transformation).
        :param mirror: If True mirrors coordinates on equator
        :param normalize: If True divides shear in pixel by total weight. If
                          set to False need to to shear = get_map('shear')
                          / get_map('weights'). Used to allow loading chunks of
                          data.
        :return: The desired maps
        """

        pixs, unis, indices = self.get_object_pixels(
            bin, alpha_rot, delta_rot, pix, mirror)

        sign_flip = True

        # construct output type
        if not isinstance(type, list):
            type = [type]
        type = ('-').join(type)

        idx = self._get_redshift_bool(bin)

        # calculate the weights map
        weights = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                           dtype=float)
        weights[unis] += np.bincount(indices, weights=self.weights[idx])
        vprint("Calculated weights", self.logger, self.verbose)

        if type == 'weights':
            return weights

        # calculate the shear maps
        shear_map_1 = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])
        shear_map_1[unis] += np.bincount(
            indices, weights=self.weights[idx] * self.gamma_1[idx])
        shear_map_2 = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])
        shear_map_2[unis] += np.bincount(
            indices, weights=self.weights[idx] * self.gamma_2[idx])

        if normalize:
            shear_map_1 /= weights
            shear_map_2 /= weights

        # masking
        mask = np.logical_not(weights > 0.0)
        shear_map_1[mask] = hp.pixelfunc.UNSEEN
        shear_map_2[mask] = hp.pixelfunc.UNSEEN

        vprint("Calculated shear maps", self.logger, self.verbose)

        if type == 'shear':
            return shear_map_1, shear_map_2
        elif (type == 'weights-shear'):
            return weights, shear_map_1, shear_map_2

        # calculate convergence maps
        m_kappa_E, m_kappa_B = self._calc_convergence_map(
            shear_map_1, shear_map_2, weights, bin,
            trimming=trimming, sign_flip=sign_flip)
        vprint("Calculated convergence maps", self.logger, self.verbose)

        if type == 'convergence':
            return m_kappa_E, m_kappa_B
        elif type == 'shear-convergence':
            return shear_map_1, shear_map_2, m_kappa_E, m_kappa_B
        elif type == 'weights-shear-convergence':
            return weights, shear_map_1, shear_map_2, m_kappa_E, m_kappa_B
        elif type == 'weights-convergence':
            return weights, m_kappa_E, m_kappa_B

    def get_mask(self, bin=0, alpha_rot=0.0, delta_rot=0.0, mirror=False):
        """
        Returns survey mask. Can optionally rotate catalog on sky.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param mirror: If True mirrors coordinates on equator
        :return: A Healpix mask (0 outside and 1 inside of mask)
        """

        weights = self.get_map('weights', bin, alpha_rot,
                               delta_rot, mirror=mirror)
        mask = weights > 0.0

        return mask

    def get_trimmed_mask(self, bin=0, alpha_rot=0.0, delta_rot=0.0,
                         mirror=False):
        """
        Given a Healpix mask creates a trimmed mask, meaning it removes some
        pixels which are distored by edge
        effects in shear->convergence procedure.
        Optionally allows rotation of catalog.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param mirror: If True mirrors coordinates on equator
        :return: The trimmed Healpix mask
        """
        mask = self.get_mask(bin=bin, alpha_rot=alpha_rot,
                             delta_rot=delta_rot, mirror=mirror)
        mask = self._trimming(mask)

        return mask

    def generate_shape_noise(self, seed=None, bin=0):
        """
        Generates shape noise which resembles the noise in the shear catalog by
        randomly rotating the shears on their locations.

        :param seed: Seeding for the random generation of the rotation.
        :param bin: Redshift bin to use (0=full sample)
        :return: The new noised shear components
        """
        idx = self._get_redshift_bool(bin)

        # Seeding
        if seed is not None:
            np.random.seed(int(seed))
            vprint("Seeded random generater with seed {}".format(
                seed), self.logger, self.verbose)

        # Draw random phase
        ell = len(self.gamma_1[idx])

        # Generate random phase
        rad, ang = self._from_rec_to_polar(
            self.gamma_1[idx] + self.gamma_2[idx] * 1j)
        ang += np.pi
        ang = (ang + np.random.uniform(0.0, 2.0 * np.pi, ell)
               ) % (2.0 * np.pi) - np.pi

        noise_shear = self._from_polar_to_rec(rad, ang)

        noise_shear_1 = np.real(noise_shear)
        noise_shear_2 = np.imag(noise_shear)

        vprint("Generated Shape Noise", self.logger, self.verbose)

        return noise_shear_1, noise_shear_2

    def generate_shape_noise_map(self, seed=None, pix=-1, bin=0,
                                 normalize=True):
        """
        Generates shape noise maps including shape noise that
        resembles the noise present in the catalog.

        :param seed: Seeding for the random generation of the rotation
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
                    instead of the actual coordinates(-1 not used, greater or
                    equal than 0 indicates the map to use)
        :param bin: Redshift bin to use (0=full sample)
        :param normalize: If True divides shear in pixel by total weight. If
                          set to False need to to shear = get_map('shear')
                          / get_map('weights'). Used to allow loading chunks of
                          data.
        :return: Two shape noise shear maps.
        """

        noise_shear_1, noise_shear_2 = self.generate_shape_noise(seed, bin)

        pixs, unis, indices = self.get_object_pixels(
            bin, alpha_rot=0.0, delta_rot=0.0, pix=pix, mirror=False)

        idx = self._get_redshift_bool(bin)

        # calulate weights maps
        weights = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                           dtype=float)
        weights[unis] += np.bincount(indices, weights=self.weights[idx])

        noise_shear_map_1 = np.zeros(
            hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
            dtype=self.ctx['prec'])
        noise_shear_map_1[unis] += np.bincount(
            indices, weights=self.weights[idx] * noise_shear_1)

        noise_shear_map_2 = np.zeros(
            hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
            dtype=self.ctx['prec'])
        noise_shear_map_2[unis] += np.bincount(
            indices, weights=self.weights[idx] * noise_shear_2)

        if normalize:
            noise_shear_map_1 /= weights
            noise_shear_map_2 /= weights

        # masking
        mask = np.logical_not(weights > 0.0)
        noise_shear_map_1[mask] = hp.pixelfunc.UNSEEN
        noise_shear_map_2[mask] = hp.pixelfunc.UNSEEN

        vprint("Generated Shape Noise map", self.logger, self.verbose)

        return noise_shear_map_1, noise_shear_map_2

    ##################################
    # HELPER FUNCTIONS
    ##################################
    def _pixelize(self, alpha, delta, bin=0, full_output=False):
        """
        Converts angular coordinates into HEalpix map
        """

        # Handling for 1 sized arrays
        if isinstance(alpha, float):
            alpha = [alpha]
        if isinstance(delta, float):
            delta = [delta]

        idx = self._get_redshift_bool(bin)

        # converting coordinates to HealPix convention
        if self.ctx['degree']:
            alpha = np.radians(alpha)
            delta = np.radians(delta)
        if not self.ctx['colat']:
            delta = np.pi / 2. - delta
        pix = hp.pixelfunc.ang2pix(self.ctx['NSIDE'], delta[idx], alpha[idx])
        pix = pix.astype(int)

        # converting coordinates back
        if self.ctx['degree']:
            alpha = np.degrees(alpha)
            delta = np.degrees(delta)
        if not self.ctx['colat']:
            delta = 90. - delta

        if full_output:
            unis, indices = np.unique(
                pix, return_inverse=True)
            return unis, indices, pix
        else:
            return pix

    def _trimming(self, mask):
        """
        Applys smoothing to a mask and removes pixels that are too far off.
        """
        mask = mask.astype(float)

        # Apply smoothing
        mask = hp.smoothing(mask, fwhm=np.radians(21.1 / 60.))

        # Only keep pixels with values in tolerance
        idx = np.abs(mask - 1.0) > 0.05

        mask[idx] = 0.0
        mask[np.logical_not(idx)] = 1.0
        mask = mask.astype(bool)
        return mask

    def _calc_convergence_map(self, shear_map_1, shear_map_2, weights, bin=0,
                              trimming=True, sign_flip=True):
        """
        calculate the convergence maps from shear maps
        """
        if sign_flip & (len(shear_map_1) > 0):
            vprint("Applying sign flip", self.logger, self.verbose)
            shear_map_1[shear_map_1 > hp.UNSEEN] *= -1.
        alm_E, alm_B = utils._calc_alms(
            shear_map_1, shear_map_2)
        if sign_flip & (len(shear_map_1) > 0):
            shear_map_1[shear_map_1 > hp.UNSEEN] *= -1.

        m_kappa_B = np.asarray(hp.alm2map(alm_B, nside=self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])
        m_kappa_E = np.asarray(hp.alm2map(alm_E, nside=self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])

        # masking
        if not trimming:
            vprint("Note: Conversion to convergence can introduce artefacts.\
            To be sure apply more conservative cut using trimmed mask.",
                   self.logger, self.verbose)
            m_kappa_E[np.logical_not(weights > 0.0)] = hp.pixelfunc.UNSEEN
            m_kappa_B[np.logical_not(weights > 0.0)] = hp.pixelfunc.UNSEEN
        else:
            mask = self._trimming(weights > 0.0)
            mask = np.logical_not(mask)
            m_kappa_E[mask] = hp.pixelfunc.UNSEEN
            m_kappa_B[mask] = hp.pixelfunc.UNSEEN

        return m_kappa_E, m_kappa_B

    def _from_rec_to_polar(self, x):
        """
        Takes a standard comlex number or sequence of
        complex numbers and return the polar coordinates.
        """
        return abs(x), np.angle(x)

    def _from_polar_to_rec(self, radii, angles):
        """
        Takes polar coordinates of a complex number or
        a sequence and returns a standard complex number.
        """
        return radii * np.exp(1j * angles)

    def _get_redshift_bool(self, bin=0):
        """
        Get the indices of the objects in a certain redshift bin.
        """
        bin = int(bin)
        if len(self.redshift_bin) == 0:
            raise Exception("Redshift bins not set. Cannot select objects")
        if bin == 0:
            idx = np.ones_like(self.redshift_bin)
        else:
            idx = np.isclose(self.redshift_bin, bin)

        if len(idx) == 0:
            raise Exception("No objects selected")
        idx = idx.astype(bool)
        return idx

    def _rotate_coordinates(self, alpha_rot, delta_rot, mirror):
        """
        rotate the coordinates
        """
        if len(self.alpha) > 0:
            alpha = self.alpha
            delta = self.delta
            # converting coordinates to HealPix convention
            if self.ctx['degree']:
                alpha = np.radians(alpha)
                delta = np.radians(delta)
            if not self.ctx['colat']:
                delta = np.pi / 2. - delta
        else:
            try:
                pix = self.pixels[0]
            except KeyError:
                raise Exception(
                    "Cannot access the pixel object and coordinates not set")
            delta, alpha = hp.pixelfunc.pix2ang(self.ctx['NSIDE'], pix)

        if mirror:
            delta = np.pi - delta

        # Healpix rotator
        rot = hp.rotator.Rotator(rot=[alpha_rot, delta_rot], deg=False)

        rot_delta, rot_alpha = rot(delta, alpha)

        if len(self.alpha) > 0:
            # converting coordinates back
            if self.ctx['degree']:
                alpha = np.degrees(alpha)
                delta = np.degrees(delta)
            if not self.ctx['colat']:
                delta = 90. - delta

        # converting rotated coordinates back
        if self.ctx['degree']:
            rot_alpha = np.degrees(rot_alpha)
            rot_delta = np.degrees(rot_delta)
        if not self.ctx['colat']:
            rot_delta = 90. - rot_delta

        vprint("Rotated coordinates by alpha=%.2f and delta=%.2f radians" %
               (alpha_rot, delta_rot), self.logger, self.verbose)
        return rot_alpha, rot_delta

    def _assert_lengths(self):
        """
        checks that the lengths of the objects are consistent
        """
        if self.store_pix:
            length = len(self.pixels[0])
        else:
            length = len(self.alpha)

        try:
            assert len(self.gamma_2) == length
            assert len(self.gamma_1) == length
            assert len(self.redshift_bin) == length
            assert len(self.weights) == length
            if not self.store_pix:
                assert len(self.delta) == length
            for k in self.pixels.keys():
                assert len(self.pixels[k]) == length
        except AssertionError:
            raise Exception(
                "Lengths of the objects passed to estats.catalog do not match")
