# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import sambuca as sb
import numpy as np
from scipy.io import loadmat
from pkg_resources import resource_filename


class TestErrorFunctions(object):

    """ Test the error functions used to assess model closure
    """

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            sb.__name__,
            'tests/data/test_error_noise.mat')
        self.__noisedata = loadmat(filename, squeeze_me=True)

        filename = resource_filename(
            sb.__name__,
            'tests/data/test_error_no_noise.mat')
        self.__data = loadmat(filename, squeeze_me=True)

    @staticmethod
    def unpack_data(data):
        return (data['observed_spectra'],
                data['modelled_spectra'],
                data['noiserrs'],
                data['num_bands'],
                data['distance_alpha'],
                data['distance_alpha_f'],
                data['distance_f'],
                data['distance_lsq'],
                data['error_a'],
                data['error_af'],
                data['error_f'])

    def validate_data(self, data):
        data_ = self.unpack_data(data)
        os = data_[0]
        ms = data_[1]
        noise = data_[2]
        num_bands = data_[3]
        assert os.shape[0] == num_bands
        assert ms.shape[0] == num_bands
        assert noise.shape[0] == num_bands
        assert noise.shape[0] == num_bands

    def test_validate_no_noise_data(self):
        self.validate_data(self.__data)

    def test_validate_noise_data(self):
        self.validate_data(self.__noisedata)

    def test_error_no_noise(self):
        os, ms, _, _, expected_distance_alpha, expected_distance_alpha_f, \
            expected_distance_f, expected_distance_lsq, expected_error_a, \
            expected_error_af, expected_error_f \
            = self.unpack_data(self.__data)

        actual_distance_alpha, actual_distance_alpha_f, \
            actual_distance_f, actual_distance_lsq, actual_error_af, \
            = sb.error_all(os, ms)

        assert np.allclose(actual_distance_alpha, expected_distance_alpha)
        assert np.allclose(actual_distance_alpha_f, expected_distance_alpha_f)
        assert np.allclose(actual_distance_f, expected_distance_f)
        assert np.allclose(actual_distance_lsq, expected_distance_lsq)
        assert np.allclose(actual_error_af, expected_error_af)

        # The IDL code was returning some identical values with different names
        # These tests ensure that we still have access to all the required
        # values
        assert np.allclose(actual_distance_alpha, expected_error_a)
        assert np.allclose(actual_distance_f, expected_error_f)

    def test_error_noise(self):
        os, ms, noise, _, expected_distance_alpha, expected_distance_alpha_f, \
            expected_distance_f, expected_distance_lsq, expected_error_a, \
            expected_error_af, expected_error_f \
            = self.unpack_data(self.__noisedata)

        actual_distance_alpha, actual_distance_alpha_f, \
            actual_distance_f, actual_distance_lsq, actual_error_af, \
            = sb.error_all(os, ms, noise)

        assert np.allclose(actual_distance_alpha, expected_distance_alpha)
        assert np.allclose(actual_distance_alpha_f, expected_distance_alpha_f)
        assert np.allclose(actual_distance_f, expected_distance_f)
        assert np.allclose(actual_distance_lsq, expected_distance_lsq)
        assert np.allclose(actual_error_af, expected_error_af)

        # The IDL code was returning some identical values with different names
        # These tests ensure that we still have access to all the required
        # values
        assert np.allclose(actual_distance_alpha, expected_error_a)
        assert np.allclose(actual_distance_f, expected_error_f)
