import numpy as np
import SimpleITK as sitk


class itk_handler(object):

    def loadImage(self, imFile):
        try:
            self.__fullImage= self.loadItkImage(imFile)
        except:
            print("Error in loading image\n")

    def saveImage(self, imFile, isVector=False):
        try:
            self.saveItkImage(imFile, self.__fullImage, isVector)
        except:
            print("Error in saving image\n")

    def getImageVolume(self):
        return self.__fullImage[0]

    def getImageOrigin(self):
        return self.__fullImage[1]

    def getImageSpacing(self):
        return self.__fullImage[2]

    def getFullImage(self):
        return self.__fullImage

    def setImageVolumage(self, vol):
        self.__fullImage[0] = vol

    def setImageOrigin(self, org):
        self.__fullImage[1] = org

    def setImageSpacing(self, sp):
        self.__fullImage[2] = sp

    def setFullImage(self,fullImage):
        self.__fullImage = fullImage

    """
     @brief: Saves an ITK image, .
     @param: fileName Name of the file to be saved.
     @param: itkImage Image to be saved. ItkImage contains image array and spatial
             coordinate details.
     @param: isVector Is the image in vector format?
     @return: NA.
     """
    @staticmethod
    def saveItkImage(fileName, itkImage, isVector=False) :
        sitk_img = sitk.GetImageFromArray(itkImage[0], isVector)
        sitk_img.SetOrigin(np.array(list(reversed(itkImage[1]))))
        sitk_img.SetSpacing(np.array(list(reversed(itkImage[2]))))
        sitk.WriteImage(sitk_img, fileName)

    """
    @brief: Reads an image.
    @param: fileName Name of the file to be read.
    @return: ItkImage contains image array and spatial coordinate details.
    """
    @staticmethod
    def loadItkImage(filename):
        itkimage = sitk.ReadImage(filename)
        vol = sitk.GetArrayFromImage(itkimage)
        origin = np.array(list(reversed(itkimage.GetOrigin())))
        spacing = np.array(list(reversed(itkimage.GetSpacing())))
        return vol, origin, spacing