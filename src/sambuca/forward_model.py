"""Semi analytical Lee/Sambuca forward model.
"""
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

import math
import numpy as np


def forward_model(
        chl,
        cdom,
        tr,
        h,
        q,
        substrate1,
        substrate2,
        wav,
        awater,
        aphy_star,
        num_bands,
        x_ph_lambda0x=0.00157747,
        x_tr_lambda0x=0.0225353,
        sc=0.0168052,
        str_=0.00977262,
        a_tr_lambda0tr=0.00433,
        y=0.878138,
        lambda0cdom=550.00,
        a_cdom_lambda0cdom=1.0,
        theta_air=30,
        offnad=10):
    """Semi analytical Lee/Sambuca forward model.

    TODO: Extended description goes here.

    Args:
        chl (float): Chlorophyll. Algal organic particles
        cdom (float): Dissolved organic particulates
        tr (float): Trypton or NAP (Non-Algal Particles)
        h (float): Depth
        q (float): Substrate proportion, used to generate a convex combination
            of substrate1 and substrate2.
        substrate1 (array-like):
        substrate2 (array-like):
        wav (array-like):
        awater (array-like): SIOP...
        aphy_star (array-like): SIOP...
        num_bands (int): number of spectral bands
        x_ph_lambda0x (float, optional):
        x_tr_lambda0x (float, optional):
        sc (float, optional):
        str_ (float, optional):
        a_tr_lambda0tr (float, optional):
        y (float, optional):
        lambda0cdom (float, optional): Reference frequency?
        a_cdom_lambda0cdom (float, optional):
        theta_air (float, optional): solar zenith
        offnad (float, optional): off-nadir angle

    Returns:
        ndarray: The modelled spectra with num_bands bands.

    """
    # pylint: disable=too-many-arguments
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals

    assert len(substrate1) == num_bands
    assert len(substrate2) == num_bands
    assert len(wav) == num_bands
    assert len(awater) == num_bands
    assert len(aphy_star) == num_bands

    thetaw = math.asin(1 / 1.333 * math.sin(math.pi / 180. * theta_air))
    thetao = math.asin(1 / 1.333 * math.sin(math.pi / 180. * offnad))

    # The wave lengths hardcoded here (550.00 and 546.00) are reference
    # wavelengths that are are actually part of the user defined SIOP set
    # TODO: 550 == lambda0cdom?
    # TODO: what is the name of the second reference frequency?
    # TODO: I think this direct port from Matlab is creating too many
    # intermediate arrays
    # TODO: some terms are reused and could be calculated just once
    bbwater = (0.00194/2.) * np.power(lambda0cdom / wav, 4.32)
    acdom_star = a_cdom_lambda0cdom * np.exp(-sc * (wav - lambda0cdom))
    atr_star = a_tr_lambda0tr * np.exp(-str_ * (wav - lambda0cdom))
    bbph_star = x_ph_lambda0x * np.power(546. / wav, y)
    bbtr_star = x_tr_lambda0x * np.power(546. / wav, y)

    a = awater + chl * aphy_star + cdom * acdom_star + tr * atr_star
    bb = bbwater + chl * bbph_star + tr * bbtr_star

    # Calculates total bottom reflectance from the two substrates and the
    # proportion of q and (1-q)
    r = q * substrate1 + (1. - q) * substrate2
    u = bb / (a + bb)
    kappa = a + bb

    du_column = 1.03 * np.power(1. + (2.4 * u), 0.5)
    du_bottom = 1.04 * np.power(1. + (5.4 * u), 0.5)

    rrsdp = (0.084 + 0.17 * u) * u
    # TODO: Ask Steve why these are unused
    # kd = kappa * (1.0 / np.cos(thetaw))
    # kuc = kappa * (du_column / np.cos(thetao))
    # kub = kappa * (du_bottom / np.cos(thetao))

    inv_cos_thetaw = 1. / math.cos(thetaw)
    du_column_scaled = du_column / math.cos(thetao)
    du_bottom_scaled = du_bottom / math.cos(thetao)
    kappa_h = kappa * h
    rrs = (rrsdp *
           (1. - np.exp(-(inv_cos_thetaw + du_column_scaled) * kappa_h)) +
           ((1. / math.pi) * r *
            np.exp(-(inv_cos_thetaw + du_bottom_scaled) * kappa_h)))

    return rrs
