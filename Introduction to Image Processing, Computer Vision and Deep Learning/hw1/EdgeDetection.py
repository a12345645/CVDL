import wx
import os
import cv2
import numpy as np
from scipy import signal

class EdgeDetection (wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.imgDict = {}

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="3.Edge Detection")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Gaussian(event):
            self. GaussianBlur()

        btn1 = wx.Button(self, label="3.1 Gaussian Blur ")
        btn1.Bind(wx.EVT_BUTTON, Gaussian)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def SobelX(event):
            self.SobelX()

        btn2 = wx.Button(self, label="3.2 Sobel X ")
        btn2.Bind(wx.EVT_BUTTON, SobelX)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def SobelY(event):
            self.SobelY()

        corner_detection = wx.Button(self, label="1.3 Sobel Y ")
        corner_detection.Bind(wx.EVT_BUTTON, SobelY)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Magnitude(event):
            self.Magnitude()

        corner_detection = wx.Button(self, label="1.4 Magnitude ")
        corner_detection.Bind(wx.EVT_BUTTON, Magnitude)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def GaussianBlur(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q3_Image/House.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        x, y = np.mgrid[-1:2, -1:2]
        kernel = np.exp(-(x**2+y**2))

        kernel = kernel / kernel.sum()

        img2 = np.zeros(img.shape)
        img = np.array(img)
        
        img2 = signal.convolve2d(img, kernel, boundary='symm', mode='same')

        img2 = img2.astype(np.uint8)
        cv2.imshow('Grayscale', img)
        cv2.imshow('Gaussian Blur', img2)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def SobelX(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q3_Image/House.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        x, y = np.mgrid[-1:2, -1:2]
        kernel = np.exp(-(x**2+y**2))

        kernel = kernel / kernel.sum()

        img2 = np.zeros(img.shape)
        img = np.array(img)
        
        img2 = signal.convolve2d(img, kernel, boundary='symm', mode='same')

        Gaussian = img2.astype(np.uint8)

        kernel = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
        img2 = signal.convolve2d(Gaussian, kernel, boundary='symm', mode='same')

        img2[img2 < 0] = 0 
        img2 = img2.astype(np.uint8)

        cv2.imshow('Sobel X', img2)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def SobelY(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q3_Image/House.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        x, y = np.mgrid[-1:2, -1:2]
        kernel = np.exp(-(x**2+y**2))

        kernel = kernel / kernel.sum()

        img2 = np.zeros(img.shape)
        img = np.array(img)
        
        img2 = signal.convolve2d(img, kernel, boundary='symm', mode='same')

        Gaussian = img2.astype(np.uint8)

        kernel = np.array([[1,2,1], [0,0,0], [-1,-2,-1]])
        img2 = signal.convolve2d(Gaussian, kernel, boundary='symm', mode='same')

        img2[img2 < 0] = 0 
        img2 = img2.astype(np.uint8)

        cv2.imshow('Sobel Y', img2)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Magnitude(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q3_Image/House.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        x, y = np.mgrid[-1:2, -1:2]
        kernel = np.exp(-(x**2+y**2))

        kernel = kernel / kernel.sum()

        img2 = np.zeros(img.shape)
        img = np.array(img)
        
        img2 = signal.convolve2d(img, kernel, boundary='symm', mode='same')

        Gaussian = img2.astype(np.uint8)

        kernel = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
        img2 = signal.convolve2d(Gaussian, kernel, boundary='symm', mode='same')

        img2[img2 < 0] = 0 
        sobelX = img2.astype(np.float32)

        kernel = np.array([[1,2,1], [0,0,0], [-1,-2,-1]])
        img2 = signal.convolve2d(Gaussian, kernel, boundary='symm', mode='same')

        img2[img2 < 0] = 0 
        sobelY = img2.astype(np.float32)

        img2 = np.sqrt(sobelX ** 2 + sobelY ** 2)
        img2 = img2.astype(np.uint8)

        cv2.imshow('Magnitude', img2)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        