# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 19:42:09 2018

@author: Gokhan Gunay
"""



import SimpleITK as sitk
import numpy as np
import sys
 
sys.path.insert(0, "./TvMin")

import TvMin
#@brief Reads an image using SimpleITK
#@param File image file to be read
#@return vol numpy array containing voxel values, origin locaitonof origin in space, spacing voxel spacing
def load_itk(File):
    itkimage = sitk.ReadImage(File)
    vol = sitk.GetArrayFromImage(itkimage)
    origin = np.array(list(reversed(itkimage.GetOrigin())))
    spacing = np.array(list(reversed(itkimage.GetSpacing())))
    return vol, origin, spacing

#@brief Reads an image file and returnes a slice 
#@param File Image file
#@param Slice Number of slice
#@return SLice of input image
def readVolumeSlice(File,Slice):
    itkimage = sitk.ReadImage(File)
    return sitk.GetArrayFromImage(itkimage)[Slice]

#@brief Reads an image file and returnes voxel intensities 
#@param File Image file to be read
#@return Image volume 
def readVolume(File):
    itkimage = sitk.ReadImage(File)
    return sitk.GetArrayFromImage(itkimage)


import matplotlib.pyplot as plt


file="./TestData/Patient04.mha"
image=readVolume(file)
print(image.shape)
tv=TvMin.TvMin()
tv.setInputImage(image)
tv.setLambda(50)
tv.setTo(0.15)
tv.setIterationNum(30)
tv.setVerbose(True)
tv.minimize()
plt.imshow(tv.getResultImage()[5], cmap="Greys_r")
plt.show()

    