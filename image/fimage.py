# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:17:54 2019

@author: Cédric Perion | Arthur Dujardin

This modules contains the necessary functions to compute the image formula for each point
"""

from os import getcwd
import  numpy as np
from inputoutput.read_xml import readCalib, readOri

def fimage(F, M, R, S) :
    """ Compute the image formula for the point M
        WITHOUT distorsion
        @param F: position of the autocollimation point in the image coordinate system
        @param M: position of the point in real space coordinates
        @param R: rotation matrix representing the orientation of the image coordinate system in the real space coordinate system
        @param S: position of the autocollimation point in the real space coordinate system
        @paramtype F: numpy.ndarray
        @paramtype M: numpy.ndarray
        @paramtype R: numpy.ndarray
        @paramtype S: numpy.ndarray
        :return: image coordinates of M projected
        :rtype: numpy.ndarray
    """
    k = np.array([0,0,1])
    R_inv = np.linalg.inv(R)
    top = k.dot(F)*R_inv.dot(M-S)
    bottom = k.dot(R_inv).dot(M-S)
    
    return F - top/bottom

def radialStd(m_image, pps, a, b, c) :
    """ Corrects the postion of the point according to the standard radial distorsion model
        @param m_image: Position of the projected point in pixel
        @param pps: position of the point of 0 distorsion ine the radialStd model
        @param a: 3rd order coefficient of the distorsion polynomial
        @param b: 5th order coefficient of the distorsion polynomial
        @param c: 7th order coefficient of the distorsion polynomial
        @paramtype m_image: numpy.ndarray
        @paramtype pps: numpy.ndarray
        @paramtype a: float
        @paramtype b: float
        @paramtype c: float
        :return: Corrected point position
        :rtype: numpy.ndarray
    """
    r = np.linalg.norm(m_image - pps)

    
    rsquared= r*r
    """ We use HORNER to evaluate ar2+br4+cr6"""
    poly = c
    poly = poly*rsquared + b
    poly = poly*rsquared + a
    poly = poly*rsquared
    """ HORNER DONE """
    dr = poly*(m_image - pps) # correction vector
    return m_image + dr

def cimage(F, M, R, S, pps, a, b, c) :
    """ Compute the image formula for the point M
        WITH distorsion
        @param F: position of the autocollimation point in the image coordinate system
        @param M: position of the point in real space coordinates
        @param R: rotation matrix representing the orientation of the image coordinate system in the real space coordinate system
        @param S: position of the autocollimation point in the real space coordinate system
        @param m_image: Position of the projected point in pixel
        @param pps: position of the point of 0 distorsion ine the radialStd model
        @param a: 3rd order coefficient of the distorsion polynomial
        @param b: 5th order coefficient of the distorsion polynomial
        @param c: 7th order coefficient of the distorsion polynomial
        @paramtype F: numpy.ndarray
        @paramtype M: numpy.ndarray
        @paramtype R: numpy.ndarray
        @paramtype S: numpy.ndarray
        @paramtype m_image: numpy.ndarray
        @paramtype pps: numpy.ndarray
        @paramtype a: float
        @paramtype b: float
        @paramtype c: float

    """
    return radialStd(fimage(F, M, R, S), pps, a, b ,c)


if __name__ == "__main__" :
    
    
    calibxml = "example/Ori-Calib/AutoCal_Foc-24000_Cam-DSLRA850.xml"
    F, pps, dist, size = readCalib(calibxml)   # F , PPS, coeffDistorsion
    print("PPS : ", pps)
    
    nameIMGxml = "example/Ori-Calib/Orientation-Im3.JPG.xml"
    R, S = readOri(nameIMGxml)   # F , PPS, coeffDistorsion
    print(R, S)
    
    M = np.transpose(np.array([984.647, 996.995, 491.721]))
    
    m  = fimage(F, M, R, S)
    print("Projection of M in the image : ", m)
    
    a, b, c = dist[0], dist[1], dist[2]
    print("radialStd : ", radialStd(m, pps, a, b, c))
    
    print("Formula image with distorsion : ", cimage(F, M, R, S, pps, a, b, c))    