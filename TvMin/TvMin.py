
import numpy as np

class TvMin(object):
    
    def __init__(self):
        self.__to = 0.15
        self.__lamb = 5
        self.__iterationNumber = 30
        self.__verbose = False
        self.__resultImage = np.array([])
    
    def getResultImage(self):
        return self.__resultImage

    def getInputImage(self):
        return self.__inputImage
    
    def setInputImage(self, inImage):                       
        self.__inputImage = inImage
    
    def setLambda(self, lamb):
        self.__lamb = lamb
    
    def setTo(self, to):
        self.__to = to
        
    def setIterationNum(self, iterationNum):
        self.__iterationNumber = iterationNum
    
    def setVerbose(self,verb):
        self.__verbose = verb
        
    def minimize(self):
        try:
            p=np.array(self.__gradient(0*self.__inputImage))
        except:
            if self.__verbose:
                print("Problem with input image")
            return
        try:
            for ind in range(0, self.__iterationNumber):
                if self.__verbose:
                    print("Itertion: ",ind)
                midP = self.__divergence(p) - self.__inputImage/self.__lamb
                psi=np.array(self.__gradient(midP))
                r = self.__getSquareSum(psi)
                p = (p + self.__to*psi)/(1 + self.__to*r)
            self.__resultImage=(self.__inputImage - self.__divergence(p)*self.__lamb)
        except:
            if self.__verbose:
                print("Problem with minimization")
    
    def __gradient(self,inImage):
        imageDimension = len(inImage.shape)
        result = []
        for ind in range(imageDimension - 1, -1,-1):
            result += [self.__forwardDerivative(inImage.swapaxes(imageDimension - 1, ind)).swapaxes(imageDimension - 1, ind)]
        return result

    def __divergence(self, inImage):
        imageDimension = len(inImage.shape) - 1
        summation = 0
        for ind in range(imageDimension - 1, -1, -1):
            summation += self.__backDerivative(inImage[imageDimension - 1 - ind].swapaxes(imageDimension - 1, ind)).swapaxes(imageDimension - 1, ind)
        return summation

    @staticmethod  
    def __getSquareSum(inImage):
        imageDimension = len(inImage.shape) - 1
        summation = 0
        for ind in range(0,imageDimension):
            summation += inImage[ind]**2
        return np.sqrt(summation)
    
    @staticmethod    
    def __forwardDerivative(In):
         d = 0*In
         d[:-1] = In[1:] - In[:-1]
         return d
    
    @staticmethod  
    def __backDerivative(In):
        d = 0*In
        d[1:] = In[1:] - In[:-1]
        return d  

    