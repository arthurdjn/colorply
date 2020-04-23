"""
This modules contains the necessary functions to compute the image formula for each "ground" point.
"""
# -*- coding: utf-8 -*-
# Created on Sun Jul 14 10:17:54 2019
# @author: Cédric Perion | Arthur Dujardin

import numpy as np


def image_formula(F, M, R, S):
    """
    Compute the image formula for the point M
    withoud distorsion

    Parameters
    ----------
    F : numpy.ndarray
        Position of the autocollimation point in the image coordinate system.
    M : numpy.ndarray
        Position of the point in real space coordinates.
    R : numpy.ndarray
        Rotation matrix representing the orientation of the image coordinate system in the real space coordinate system.
    S : numpy.ndarray
        Position of the autocollimation point in the real space coordinate system.

    Returns
    -------
    numpy.ndarray
        Image coordinates of M projected.

    """
    k = np.array([0, 0, 1])
    R_inv = np.linalg.inv(R)
    top = k.dot(F) * R_inv.dot(M - S)
    bottom = k.dot(R_inv).dot(M - S)

    return F - top / bottom


def radial_std(m_image, pps, a, b, c):
    r"""
    Corrects the postion of the point according
    to the standard radial distorsion model.

    .. note::
        We use Horner's method to evaluate :math:`ar^2 + br^4 + cr^6`

    Parameters
    ----------
    m_image : numpy.ndarray
        Position of the projected point in pixel.
    pps : numpy.ndarray
        Position of the point of 0 distorsion in the radial model.
    a : float
        3rd order coefficient of the distorsion polynomial.
    b : float
        5th order coefficient of the distorsion polynomial.
    c : float
        7th order coefficient of the distorsion polynomial.

    Returns
    -------
    numpy.ndarray
        Corrected point position.

    """
    r = np.linalg.norm(m_image - pps)
    rsquared = r * r

    # Horner's method
    poly = c
    poly = poly * rsquared + b
    poly = poly * rsquared + a
    poly = poly * rsquared

    # Correction vector
    dr = poly * (m_image - pps)

    return m_image + dr


def image_formula_corrected(F, M, R, S, pps, a, b, c):
    """
    Compute the image formula for the point M
    with distorsion.

    Parameters
    ----------
    F : numpy.ndarray
        Position of the autocollimation point in the image coordinate system.
    M : numpy.ndarray
        Position of the point in real space coordinates.
    R : numpy.ndarray
        Rotation matrix representing the orientation of the image coordinate system in the real space coordinate system.
    S : numpy.ndarray
        Position of the autocollimation point in the real space coordinate system.
    pps : numpy.ndarray
        Position of the point of 0 distorsion ine the radial_std model.
    a : float
        3rd order coefficient of the distorsion polynomial.
    b : float
        5th order coefficient of the distorsion polynomial.
    c : float
        7th order coefficient of the distorsion polynomial.

    Returns
    -------
    numpy.ndarray
        Corrected point position.

    """
    return radial_std(image_formula(F, M, R, S), pps, a, b, c)
