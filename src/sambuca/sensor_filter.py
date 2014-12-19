''' Sambuca Sensor Filtering
'''
# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
from builtins import *

import numpy as np


def sensor_filter_ml(spectra, filter_):
    # TODO: fix this function description. My attempt babbles!
    """sensor_filter_ml
    Sensor filter, resamples the input spectra using the spectral
    response function.

    :param spectra: the input spectra
    :param filter_: spectral response function
    """

    return np.dot(spectra, filter_) / filter_.sum(0)