# -*- coding: utf-8 -*-
# Created on Sun Jul 14 10:17:54 2019
# @author: Cédric Perion | Arthur Dujardin

"""
This modules contains the necessary functions to compute the image formula for each "ground" point.
"""

import  numpy as np



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

    k = np.array([0,0,1])
    R_inv = np.linalg.inv(R)
    top = k.dot(F)*R_inv.dot(M-S)
    bottom = k.dot(R_inv).dot(M-S)
    
    return F - top/bottom

def radial_std(m_image, pps, a, b, c):
    """
    Corrects the postion of the point according to the standard radial distorsion model.
    

    Parameters
    ----------
    m_image : numpy.ndarray
        Position of the projected point in pixel.
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

    r = np.linalg.norm(m_image - pps)

    rsquared= r*r
    # We use HORNER to evaluate ar2+br4+cr6
    poly = c
    poly = poly*rsquared + b
    poly = poly*rsquared + a
    poly = poly*rsquared
    # HORNER DONE
    # Correction vector
    dr = poly*(m_image - pps) 
    
    return m_image + dr

def image_formula_corrected(F, M, R, S, pps, a, b, c) :
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
    
    return radial_std(image_formula(F, M, R, S), pps, a, b ,c)


if __name__ == "__main__" :
    from colorply import io

    
    calibxml = "example/Ori-Calib/AutoCal_Foc-24000_Cam-DSLRA850.xml"
    F, pps, dist, size = io.readCalib(calibxml)   # F , PPS, coeffDistorsion
    print("PPS : ", pps)
    
    nameIMGxml = "example/Ori-Calib/Orientation-Im3.JPG.xml"
    R, S = io.readOri(nameIMGxml)   # F , PPS, coeffDistorsion
    print(R, S)
    
    M = np.transpose(np.array([984.647, 996.995, 491.721]))
    
    m  = image_formula(F, M, R, S)
    print("Projection of M in the image : ", m)
    
    a, b, c = dist[0], dist[1], dist[2]
    print("radial_std : ", radial_std(m, pps, a, b, c))
    
    print("Formula image with distorsion : ", image_formula_corrected(F, M, R, S, pps, a, b, c))    