# -*- coding: utf-8 -*-
# Created on Sat Jul 13 20:53:48 2019
# @author: arthurd


""" 
This module recieves instruction from the ui and call the appropriate 
functions on the appropriate parameters.
"""

import os


def getImgFromDir(dirPath):
    files = []
    for r, d, f in os.walk(dirPath):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    return files
