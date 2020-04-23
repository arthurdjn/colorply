# -*- coding: utf-8 -*-
# Created on Sun Jul 14 10:17:54 2019
# @author: Cédric Perion | Arthur Dujardin

"""
Module to preprocess images.
"""

import random
import numpy as np
import math

from colorply import process
from colorply import io


def radiometry_projection(M, images_loaded, calibration, mode="avg", scale=0.0038909912109375):
    """
    This function add to a point M a new channel, computed from the loaded images.
    Therefore, the images should be calibrated in the same reference of your point M.
    Usually, the 3D point M is part of a cloud points.
    The point M is projected in all images that see the point. Then, the radiometry from
    the images channel is added to the point, with different mode.

    Parameters
    ----------
    M : numpy.ndarray
        Position of the point in real space coordinates.
    images_loaded : list of Images
        List of the image loaded. 
        These images need to be referenced in the same system as the point M.
        Usually with MicMac calibrate all the images together.
    calibration : list
        List containing the camera calibration global parameters.
    mode : str, optional
        The way the new radiometry is stacked in the new M channel. 
        This can be with a mean of all radiometry that see the 3D point M. 
        The default is "avg".
    scale : float
        Used to scale a channel to [0, 255] values.
        For Sequoia camera, use a scale factor of 0.0038909912109375.

    Returns
    -------
    float
        Value of the new channel.
    """

    if mode == "avg":
        n = len(images_loaded)
        L = []
        for i in range(n):

            img = images_loaded[i]
            size = calibration[3]  # IMAGE size, coordinate i,j != x,y
            data = img.data
            R = img.R
            S = img.S
            F = calibration[0]
            pps = calibration[1]
            a = calibration[2][0]
            b = calibration[2][1]
            c = calibration[2][2]

            m = process.image_formula_corrected(F, M, R, S, pps, a, b, c)
            mx = int(np.round(m[0]))
            my = int(np.round(m[1]))

            if (0 < mx < size[0]) and (0 < my < size[1]):  # because i,j != x,y
                L.append(int(data[my, mx] * scale))

        if len(L) != 0:
            return mean(L)

    elif mode == "alea":
        return alea(M, images_loaded, calibration)

    elif mode == "":
        pass
        # ajouterfonctions

    return 0


def add_cloud_channel(input_ply, calibration_file, orientation_dir, image_dir, image_ext, channel, mode, output_ply,
                      progress=None):
    """
    All together. Project all points from a ply file.

    Parameters
    ----------
    input_ply : plydata
        The cloud points to add a new channel.
    calibration_file : str
        Path to the MicMac calibration file.
    orientation_dir : str
        Path to the MicMac images orientation directory.
    image_dir : str
        Path to the images with the channel to add.
    image_ext : str
        Images extension (JPG, TIFF, PNG etc.).
    channel : str
        Channe name.
    mode : str
        Way to add the new radiometry to the cloud points.
    output_ply : plydata
        The output cloud points, with the new channel.
    progress : PyQt progress bar
        The bar of progress.
        The default is None.

    Raises
    ------
    FileNotFoundError
        If files are not found, raise an error.

    Returns
    -------
    Bool
        Return True when done.

    """
    try:
        calxml = io.read_calib(calibration_file)
        plydata = io.read_plyfile(input_ply)
    except FileNotFoundError:
        raise FileNotFoundError
    cloudData = io.plydata_to_array(plydata)
    list_new_radiometry = []
    n = len(cloudData)

    if progress is not None:
        progress.setMaximum(100)

    images_loaded = io.load_images(orientation_dir, image_dir, image_ext, channel)

    q = n // 100

    for i in range(n):
        M = cloudData[i, 0:3]  # Collect the XYZ informations from the numpy cloud
        radiometry = radiometry_projection(M, images_loaded, calxml, mode)
        list_new_radiometry.append(radiometry)

        # Update the PyQt progress bar thread
        if progress is not None:
            if (i % q) == 0:
                progress.setValue(i // q)

    io.write_plydata(plydata, list_new_radiometry, channel, output_ply)

    # Update the PyQt progress bar thread
    if progress is not None:
        progress.setValue(100)

    return True


# TODO: in a seaparate file, functional.py
# Functional functions, used as mode to merge radiometries

def mean(L):
    return int(sum(L) / len(L))


def alea(M, images_loaded, calibration):
    radio = []
    size = calibration[3]
    n = len(images_loaded)
    for i in range(n):
        image = images_loaded[i]
        size = calibration[3]  # IMAGE size, coordinate i,j != x,y
        data = image.data
        R = image.R
        S = image.S
        F = calibration[0]
        pps = calibration[1]
        a = calibration[2][0]
        b = calibration[2][1]
        c = calibration[2][2]

        m = image.image_formula_corrected(F, M, R, S, pps, a, b, c)

        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1], m[0]])
    return random.choice(radio)


def distance(M, S, images_loaded, calibration):
    radio = []
    dist = []
    size = calibration[3]
    n = len(images_loaded)
    for i in range(n):
        m = radiometry_projection(M, images_loaded[i], calibration)
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            dist.append(np.linalg.norm(S - M))
            data = images_loaded[i].data
            radio.append(data[m[1], m[0]])
            index = dist.index(min(dist))
    return radio[index]


def distance_center(M, images_loaded, calibration):
    distcentre = []
    radio = []
    size = calibration[3]
    n = len(images_loaded)
    for i in range(n):
        m = radiometry_projection(M, images_loaded[i], calibration)  ## a changer
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1], m[0]])
            dist = (m[0] - size[0] / 2) ** 2 + (m[1] - size[1] / 2) ** 2
            distcentre.append(dist)
    index = distcentre.index(min(distcentre))
    return radio[index]


def scalar(M, images_loaded, calibration):
    scal = []
    radio = []
    size = calibration[3]
    F = calibration[0]
    n = len(images_loaded)
    for i in range(n):
        m = radiometry_projection(M, images_loaded[i], calibration)
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1], m[0]])
            angle = math.acos(F[2] / (math.sqrt((F[0] - m[0]) ** 2 + (F[1] - m[1]) ** 2 + F[2] ** 2)))
            scal.append(angle)
    index = scal.index(min(scal))
    return radio[index]


def weighted_mean(M, images_loaded, calibration):
    # A debuger+ cas 1 valeur (NIR OU RED OU GREEn...) (et non R V B !!!)

    moy = mean(M, images_loaded, calibration)
    avg_radiometry = 0
    compt = 0
    size = calibration[3]
    n = len(images_loaded)

    for i in range(n):
        m = radiometry_projection(M, images_loaded[i], calibration)
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            if data[m[1], m[0]].all() != moy.all():  # dans le de RVB, donc à mmodifier
                avg_radiometry += (1 / abs(moy - data[m[1], m[0]])) * data[m[1], m[0]]

                compt += 1 / abs(moy - data[m[1], m[0]])

            else:
                avg_radiometry = data[m[1], m[0]]
                compt += 1

    return avg_radiometry / compt


if __name__ == "__main__":
    calibxml = "../../test/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-GRE.xml"
    calibration = io.read_calib(calibxml)  # F , PPS, coeffDistorsion
    # print(calibration)
    M = np.array([984.647, 996.995, 491.721])

    images_loaded = io.load_images(orientation_dir="../../test/Ori-1bande_All_CampariGCP",
                                   image_dir="../../test/GRE",
                                   image_ext="TIF",
                                   channel="GREEN")
    # print(images_loaded)

    img = images_loaded[0]
    print(img.name)
    # print(image.R)

    input_ply = "../../test/RVB_GRE.ply"
    calibration_file = calibxml
    orientation_dir = "../../test/Ori-1bande_All_CampariGCP"
    image_dir = "../../test/RED"
    image_ext = "TIF"
    channel = "RED"
    mode = "avg"
    output_ply = "test.ply"

    add_cloud_channel(input_ply,
                      calibration_file,
                      orientation_dir,
                      image_dir,
                      image_ext,
                      channel,
                      mode,
                      output_ply,
                      progress=None)

    # print(radiometry_projection(M, images_loaded, calibration))
    # print(mean(M, images_loaded, calibration))
    # print(random(M, images_loaded, calibration))
    # print(distance(M,image.S, images_loaded, calibration))
    # print(distance_center(M, images_loaded, calibration))
    # print(scalar(M,images_loaded,calibration))
    # print(weighted_mean(M,images_loaded,calibration))
