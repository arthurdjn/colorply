# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:17:54 2019

@author: Cédric Perion | Arthur Dujardin
"""


import numpy as np
import matplotlib.pyplot as plt

from fimage import cimage
from inputoutput.read_xml import readOri, readCalib
from image import Image


#Import path to read files in a directory
from os import listdir
from os import getcwd
from os.path import isfile, join



def loadImages(outOri, dirName = "", ext = ".jpg", channel = "unknown") :
    """ 
    Reads all images and returns a list of images
    """
    dirPath = getcwd() + "\\" + dirName
    files = [f for f in listdir(dirPath) if (isfile(join(dirPath, f)) and f[len(f)-4:len(f)] == ext)]
    
    images_loaded = []
    for k in range(len(files)):
        xmlfile = dirPath + "\\" + "Ori-" + outOri + "\\Orientation-" + files[k] + ".xml"
        R, S = readOri(xmlfile)      
        images_loaded.append(Image((files[k]), channel, plt.imread(dirName + "\\" + files[k]), R, S))
        
    
        

    return images_loaded





def computeRadiometryProjection(M, images_loaded, calibration, mode = "avg"):
    n = len(images_loaded)
    for i in range(n):
        image = images_loaded[i]
        data = image.data
        R = image.R
        S = image.S
        
        size = calibration[3]
        
        F = calibration[0]
        pps = calibration[1]
        a = calibration[2][0]
        b = calibration[2][1]
        c = calibration[2][2]
        m = cimage(F, M, R, S, pps, a, b, c,)
        
        if mode.lower() == "avg":
            avg_radiometry = 0
            compt = 0
            
            mx = int(np.round(m[0]))
            my = int(np.round(m[1]))
            if ((0 < mx < size[0]) and (0 < my < size[1])):
                print(int(np.round(m[0])), int(np.round(m[1])))
                avg_radiometry += data[my, mx]
                compt += 1
        else:
            print("The mode is unknown. Please change it by : avg")
            return 0
        avg_radiometry = avg_radiometry/compt
        return avg_radiometry




if __name__ == "__main__" :
    
    
    calibxml = "example\\Ori-Calib\\AutoCal_Foc-24000_Cam-DSLRA850.xml"
    calibration = readCalib(calibxml)   # F , PPS, coeffDistorsion
    print(calibration)
    M = np.array([984.647, 996.995, 491.721])

    images_loaded = loadImages("Calib", "example", ".jpg", "red")
    print(images_loaded)
    
    
    image = images_loaded[0]
    print(image.name)
    print(image.R)

    print(computeRadiometryProjection(M, images_loaded, calibration))

    
    
    