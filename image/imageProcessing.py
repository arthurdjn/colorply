# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:17:54 2019

@author: Cédric Perion | Arthur Dujardin
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import math

from image.fimage import cimage
from inputoutput.read_xml import readOri, readCalib
from image.image import Image
from inputoutput.ply import *
from inputoutput.imagefile import *
from inputoutput.imagefile import loadImages

#Import path to read files in a directory
from os import listdir
from os import getcwd
from os.path import isfile, join




def computeRadiometryProjection(M, images_loaded, calibration, mode = "avg"):
    if mode == "avg" :
        n = len(images_loaded)
        L = []
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
            
            m = cimage(F, M, R, S, pps, a, b, c)
            mx = int(np.round(m[0]))
            my = int(np.round(m[1]))

               
            if (0 < mx < size[0]) and (0 < my < size[1]):  # because i,j != x,y
                L.append(int(data[my, mx]*0.0038909912109375))
                
        if len(L) != 0:
            return mean(L)
    
    elif mode == "alea":    
        return aleatoire(M,images_loaded,calibration)
    
    elif mode == "":
        pass
            
            #ajouterfonctions
    
    return 0       
    
    
   
def addChannelToCloud(inPly, calFile, ori, imDir, imExt, channel, mode, outPly, progress):
    """
    channelCloud = all, RED, NIR....
    tell witch of the channel to keep from the cloud 
    because mono channel cloud are 3 components (R, V, B = grey), so we need to have only one information
    in that case
    """
    try :
        calxml = readCalib(calFile)
        plydata = readply(inPly)
    except FileNotFoundError :
        raise FileNotFoundError
    cloudData = convertCoordinatesPlyArray(plydata)
    listNewRadiometry = []
    n=len(cloudData)
    progress.setMaximum(n)
    images_loaded = loadImages(ori, imDir, imExt, channel)
    for i in range(n):
        M = cloudData[i, 0:3] #Collect the XYZ informations from the numpy cloud
        radiometry = computeRadiometryProjection(M, images_loaded, calxml, mode)
        listNewRadiometry.append(radiometry)
        progress.setValue(i)
        
    newCloud = writeply(plydata, listNewRadiometry, channel, outPly)
    progress.setValue(n)
    print(listNewRadiometry)
    return 1
    
    
    
    
    
    
    
    
    
    
    
def mean(L):
    return int(sum(L)/len(L))

def aleatoire(M,images_loaded,calibration):
    radio=[]        
    size = calibration[3]
    n=len(images_loaded)
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
        
        m = cimage(F, M, R, S, pps, a, b, c)
        
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1],m[0]])
    return random.choice(radio)


def distance(M,S,images_loaded,calibration):
    radio=[]
    dist=[]
    size = calibration[3]
    n=len(images_loaded)
    for i in range(n):
        m=computeRadiometryProjection(M,images_loaded[i],calibration)  
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
                dist.append(np.linalg.norm(S-M))
                data = images_loaded[i].data
                radio.append(data[m[1],m[0]])
                index=dist.index(min(dist))
    return radio[index]
            
def distanceCentre(M,images_loaded,calibration):
    distcentre=[]
    radio=[]
    size = calibration[3]
    n=len(images_loaded)
    for i in range(n):
        m=computeRadiometryProjection(M,images_loaded[i],calibration) ## a changer 
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1],m[0]])
            dist=(m[0]-size[0]/2)**2+(m[1]-size[1]/2)**2
            distcentre.append(dist)        
    index=distcentre.index(min(distcentre))        
    return radio[index]

def scalaire(M,images_loaded,calibration):
    scal=[]
    radio=[]
    size = calibration[3]
    F=calibration[0]
    n=len(images_loaded)
    for i in range(n):
        m=computeRadiometryProjection(M,images_loaded[i],calibration)  
        if ((0<m[0]<size[0]) and (0<m[1]<size[1])):
            data = images_loaded[i].data
            radio.append(data[m[1],m[0]])
            angle=math.acos(F[2]/(math.sqrt((F[0]-m[0])**2+(F[1]-m[1])**2+F[2]**2)))
            scal.append(angle)
    index=scal.index(min(scal))
    return radio[index]

def meanPonderation(M,images_loaded,calibration):
    #A debuger+ cas 1 valeur (NIR OU RED OU GREEn...) (et non R V B !!!)
    
    moy=mean(M,images_loaded,calibration)
    avg_radiometry=0
    compt=0
    size = calibration[3]
    n=len(images_loaded) 
    
    for i in range(n):
        m=computeRadiometryProjection(M,images_loaded[i],calibration)  
        if ((0 < m[0] < size[0]) and (0 < m[1] < size[1])):
            data = images_loaded[i].data
            if data[m[1], m[0]].all() != moy.all():   # dans le de RVB, donc à mmodifier
                avg_radiometry += (1/abs(moy - data[m[1], m[0]]))*data[m[1], m[0]]
                
                compt += 1/abs(moy - data[m[1], m[0]])
                
            else:
                avg_radiometry = data[m[1], m[0]]
                compt += 1

                   
    return avg_radiometry/compt

if __name__ == "__main__" :        
    calibxml = "example/Ori-Calib/AutoCal_Foc-24000_Cam-DSLRA850.xml"
    calibration = readCalib(calibxml)   # F , PPS, coeffDistorsion
    #print(calibration)
    M = np.array([984.647, 996.995, 491.721])

    images_loaded = loadImages("Calib", "example", ".jpg", "red")
    #print(images_loaded)
    
    image = images_loaded[0]
    print(image.name)
    #print(image.R)

    #print(computeRadiometryProjection(M, images_loaded, calibration))
    print(mean(M, images_loaded, calibration))
    #print(aleatoire(M, images_loaded, calibration))
    #print(distance(M,image.S, images_loaded, calibration))
    #print(distanceCentre(M, images_loaded, calibration))
    #print(scalaire(M,images_loaded,calibration))
    print(meanPonderation(M,images_loaded,calibration))
   