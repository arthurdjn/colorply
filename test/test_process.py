# -*- coding: utf-8 -*-
# Created on Sat Feb  8 14:21:19 2020
# @author: arthurd


import numpy as np
import matplotlib.pyplot as plt

# Colorply package
from colorply import process
from colorply import io


def test_image():
    
    print("\nMaking an image...")
    orientation_file = "data/Ori-1bande_All_CampariGCP/Orientation-IMG_190716_082134_0016_REG.TIF.xml"
    image_file = "data/REG/IMG_190716_082134_0016_REG.TIF"
    R, S = io.read_ori(orientation_file)
    data = plt.imread(image_file)
    image = process.Image(image_file, "REG", data, R, S)
    
    print("Image created.")
    print("The name of the image is :\n", image.name)
    print("The channel of the image is :\n", image.channel)
    print("The data of the image is :\n", image.data)
    print("The rotation of the image is :\n", image.R)
    print("The top of the image is :\n", image.S)


def test_radiometry_projection():
    
    print("\nProjecting a point...")
    M = np.array([2.86285281181335449, 904.19775390625, 686.24530029296875])
    
    calibration_file = "data/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-GRE.xml"
    orientation_dir = "data/Ori-1bande_All_CampariGCP"
    image_dir = "data/GRE"
    image_ext = "TIF"
    channel = "GREEN"
    
    calibration = io.read_calib(calibration_file)
    images_loaded = io.load_images(orientation_dir = orientation_dir,
                                   image_dir = image_dir,
                                   image_ext = image_ext,
                                   channel = channel)
    radiometry = process.radiometry_projection(M, images_loaded, calibration, mode = "avg")
    print("Point projected.\nRadiometry added : {0}".format(radiometry))


def test_add_channel():

    print("\nAdding channel to ply file...")
    input_ply = "data/RVB_GRE.ply"
    calibration_file = "data/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-GRE.xml"
    orientation_dir = "data/Ori-1bande_All_CampariGCP"
    image_dir = "data/RED"
    image_ext = "TIF"
    channel = "RED"
    mode = "avg"
    output_ply = "test_process.ply"

    process.add_cloud_channel(input_ply, 
                      calibration_file, 
                      orientation_dir, 
                      image_dir, 
                      image_ext, 
                      channel, 
                      mode, 
                      output_ply, 
                      progress = None)
    print("Channel added")
    
    
    
if __name__ == "__main__":
    
    # Test image
    test_image()
    
    # Projecting a single point
    test_radiometry_projection()
    
    # Test adding channel to ply cloud
    test_add_channel()
    
    
    
    
    