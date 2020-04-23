# -*- coding: utf-8 -*-
# Created on Sat Feb  8 12:50:37 2020
# @author: arthurd


import matplotlib.pyplot as plt

from os import listdir, sep
from os.path import isfile, join
from colorply.mm3d import read_ori
from colorply.process.image import Image


def load_images(orientation_dir, image_dir=".", image_ext="TIF", channel="unk"):
    """ 
    Reads all images and returns a list of image objects
    
    """
    try:
        files = [f for f in listdir(image_dir) if (isfile(join(image_dir, f)) and f.split('.')[-1] == image_ext)]
    except FileNotFoundError:
        raise FileNotFoundError('The images were not found.')

    images_loaded = []

    for file in files:
        # Load the orientation
        orixml = orientation_dir + sep + "Orientation-" + file + ".xml"
        ori = read_ori(orixml)
        R, S = ori['R'], ori['S']

        # Load the data
        data = plt.imread(image_dir + sep + file)
        img = Image(file, channel, data, R, S)

        # Store it to a list
        images_loaded.append(img)

    return images_loaded


if __name__ == "__main__":
    print(load_images(orientation_dir="../../test/Ori-1bande_All_CampariGCP",
                      image_dir="../../test/GRE",
                      image_ext="TIF")
          )
