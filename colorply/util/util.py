# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:17:54 2019

@author: Cédric Perion | Arthur Dujardin

Contains various useful functions
"""

import plyfile

def toascii(inputFile, outPutfile) :
    el = plyfile.PlyData.read(inputFile)
    el2 = plyfile.PlyElement.describe(el.elements[0].data, 'vertex')
    plyfile.PlyData([el2], text=True).write(outPutfile)

