from os import getcwd
import numpy as np
from image.image import *
from image.imageProcessing import *
from image.fimage import *
from inputoutput.read_xml import *
from util.util import *
from inputoutput.ply import *
from ui.gui import *
from ui.call import *
from ui.palette import *




runMainWindow()











"""
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
"""


"""
cloudPath = "C3DC_QuickMac_1bandeAllCampariGCP_5images_SMALL.ply"
plydata = readply(cloudPath)


calibration = "example/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-NIR.xml"
calibration = readCalib(calibration)


outOri = "1bande_All_CampariGCP"
dirName = "example"
ext = ".TIF"
channelImages = "NIR"
mode = "avg"


addChannelToCloud(cloudPath, calibration, outOri, dirName, ext, channelImages, mode)
"""




