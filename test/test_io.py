# -*- coding: utf-8 -*-
# Created on Sat Feb  8 14:22:52 2020
# @author: arthurd


import numpy as np

from colorply import io



def test_calib():
    
    print("\nLoad calibration...")
    calibration_file = "data/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-REG.xml"
    xmlfile = "data/Ori-1bande_All_CampariGCP/Orientation-IMG_190716_082134_0016_REG.TIF.xml"
    
    # 1/ Matrix Rotation
    print("The rotation matrix of the image " + xmlfile + " is : \n", io.read_orientation(xmlfile)) 
    # 2/ Center S of the IMG
    print("\nThe image's center is : \n", io.read_S(xmlfile))
    # 2.5/ Opti read Orientation
    print("\nThe orientation and center of the image are :\n", io.read_ori(xmlfile),"\n")
    # 3/ F focale
    print("\nThe F point from the camera " + calibration_file + " is : \n", io.read_calib_F(calibration_file))
    # 4/ PPS 
    print("\nThe PPS from the camera " + calibration_file + " is : \n", io.read_calib_PPS(calibration_file))
    # 5/ PPS 
    print("\nThe coefficients a, b, c from the camera " + calibration_file + " is : \n", io.read_calib_distorsion(calibration_file))
    # 6/ Opti param
    print("\nThe calibration parameters of this image are : \n", io.read_calib(calibration_file))


def test_load_images():
        
    orientation_dir = "data/Ori-1bande_All_CampariGCP"
    image_dir = "data/GRE"
    image_ext = "TIF"
    channel = "GREEN"
    
    print("\nLoading images...")
    images_loaded = io.load_images(orientation_dir = orientation_dir,
                                   image_dir = image_dir,
                                   image_ext = image_ext,
                                   channel = channel)
    print("Images loaded :")
    print([img.name for img in images_loaded])
    
    
def test_ply():
    file_name = "data/RVB_GRE.ply"
    plydata = io.read_plyfile(file_name)
    
    #1/ Converting the plydata to an array
    data = io.plydata_to_array(plydata)
    print("The data from the plydata is :\n", data)
    
    #2/ Adding channel
    channel = "green"
    data2 = io.add_channel_from_plydata(plydata, data, channel)
    print("\nAdding the channel ", channel, " to the data :\n", data2)
    # Adding random channel
    n = len(plydata.elements[0].data['x'])
    newChannel = np.random.randint(n*[255])
    channel2 = np.array(newChannel)
    print(channel2)
    print("Test writing")
    data = io.write_plydata(plydata, channel2, 'test', "test_io.ply")
    
    
    
    
    
if __name__ == "__main__":
    
    # Load the calibration file
    test_calib()
    
    # Load images
    test_load_images()
    
    # Test creating ply files
    test_ply()
    
    
    