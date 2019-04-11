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
print(Sn.shape)
#Sn=Sn[5]
#Im=scipy.ndimage.imread(File, flatten=False, mode=None)
#Im=np.array(Im[:,:,0],dtype="float")

sizeArray=np.array(Sn.shape)
#addition of padding to image edges
sizeArray+=2
imArr=np.zeros(sizeArray)
imArr[1:-1,1:-1,1:-1]=Sn
Sn=imArr
print(Sn.shape)

def der(In):
    D=0*In
    D[:-1]=In[1:]-In[:-1]
    return D

def div1(In):
    div=0*In
    div[1:]=In[1:]-In[:-1]
    return div

def gradient(inImage):
    imageDimension=len(inImage.shape)
    print(inImage.shape)
    print(imageDimension)
    result=[]
    for ind in range(imageDimension-1,-1,-1):
        print(ind)
        result+=[der(inImage.swapaxes(imageDimension-1,ind)).swapaxes(imageDimension-1,ind)]
    return result

def divergence(inImage):
    imageDimension=len(inImage.shape)-1
    print((imageDimension))
    
    summation=0
    for ind in range(imageDimension-1,-1,-1):
        summation+=div1(inImage[imageDimension-1-ind].swapaxes(imageDimension-1,ind)).swapaxes(imageDimension-1,ind)
        
    return summation

    

def derX(In):
    D=0*In
    D[:-1,:,:]=In[1:,:,:]-In[:-1,:,:]
    return D

def derY(In):
    D=0*In
    D[:,:-1,:]=In[:,1:,:]-In[:,:-1,:]
    return D

def derZ(In):
    D=0*In
    D[:,:,:-1]=In[:,:,1:]-In[:,:,:-1]
    return D

def grad(In):
    return derX(In),derY(In),derZ(In)

def divZ(In):
    DivX=1*In
    DivX[:,:,1:]=In[:,:,1:]-In[:,:,:-1]
    return DivX

def divY(In):
    Div=0*In
    Div[:,1:,:]=In[:,1:,:]-In[:,:-1,:]
    return Div

def divX(In):
    Div=0*In
    Div[1:,:,:]=In[1:,:,:]-In[:-1,:,:]
    return Div

def div(In):
    return divX(In[0])+divY(In[1])+divZ(In[2])


Pold=np.array([np.copy(Sn),np.copy(Sn),np.copy(Sn)])
P=0*Pold
To=0.1
Lm=50.0001
for ii in range(0,20):
    Psi=np.array(gradient(divergence(P)-Sn/Lm))
    r=np.sqrt(Psi[0]**2+Psi[1]**2+Psi[2]**2)
    P=(P+To*Psi)/(1+To*r)
    
Sest=(Sn-divergence(P)*Lm)
plt.imshow(Sest[5],cmap="Greys_r")
#plt.imshow(np.abs(Sn-Sest),cmap="Greys_r")
plt.show()
    



