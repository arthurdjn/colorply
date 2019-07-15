# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:17:54 2019

@author: Cédric Perion | Arthur Dujardin
"""

import numpy as np
import matplotlib.pyplot as plt
import inputoutput.read_xml as read_xml



class Image :
    
    def __init__(self, name = "None", channel = "None", data = np.array([[]]), R = np.eye(3), S = np.transpose(np.array([0,0,0])) ):
        self.name = name
        self.channel = channel
        self.data = data
        self.R = R
        self.S = S



if __name__ == "__main__" :
    print("***** Welcome *****\nThis script defines the class Image\n\n")
    
    xmlfile = "example\\Ori-Calib\\Orientation-Im3.JPG.xml"
    R, S = read_xml.readOri(xmlfile)
    image = Image("example\\Im3.JPG", "red", plt.imread("example\\Im3.JPG"), R, S)
    
    print("The name of the image is : ", image.name, "\n")
    print("The channel of the image is : ", image.channel, "\n")
    print("The data of the image is : \n", image.data, "\n")
    print("The rotation of the image is \n: ", image.R, "\n")
    print("The top of the image is : ", image.S, "\n")
    
    
    
    
    
    
    