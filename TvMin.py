#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 19:42:09 2018

@author: gogo
"""



import SimpleITK as sitk
import numpy as np


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


#import skimage
#skimage



#import scipy.ndimage
import matplotlib.pyplot as plt


file="/hdd/Mega/Dropbox_old_2/Dataset/Pre.mhd"

Sn=readVolume(file)
Sn=Sn[5]
#Im=scipy.ndimage.imread(File, flatten=False, mode=None)
#Im=np.array(Im[:,:,0],dtype="float")





def derX(In):
    Dx=0*In
    Dx[:-1]=In[1:]-In[:-1]
    return Dx

def grad(In):
    return derX(In.T).T,derX(In)

def divX(In):
    DivX=1*In
    DivX[1:]=In[1:]-In[:-1]#DivX[1:-1]=In[1:-1]-In[:-2]
    #DivX[-1]=-In[-2]
    return DivX

def div(In):
    return divX(In[0].T).T+divX(In[1])


Pold=np.array([np.copy(Sn),np.copy(Sn)])
P=0*Pold
To=0.1
Lm=25.0001
for ii in range(0,100):
#while np.max(np.sqrt((P[0]-Pold[0])**2+(P[1]-Pold[1])**2))>0.00000005:
    Psi=np.array(grad(div(P)-Sn/Lm))
    r=np.sqrt(Psi[0]**2+Psi[1]**2)
    P=(P+To*Psi)/(1+To*r)
    
Sest=(Sn-div(P)*Lm)
plt.imshow(Sest,cmap="Greys_r")
#plt.imshow(np.abs(Sn-Sest),cmap="Greys_r")
plt.show()





"""
St=10000
P=0*Sn
Pold=np.copy(Sn)
To=0.25
Lm=100
while np.max(np.abs(P-Pold))>0.000005:
    Psi=(derX(divX(P)-Sn/Lm))
    r=np.sqrt(np.sum(Psi**2))
    Pold=1*P
    P=(Pold+To*Psi)/(1+To*r)
    
Sest=(Sn-divX(P)*Lm)
plt.plot(Sest[:256])
"""
    



