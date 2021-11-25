import wx
import os
import cv2
import numpy as np
import pprint

from wx.core import EAST

class ImageProcessing(wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.imgDict = {}

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="1.Image Processing")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  LoadImage(event):
            self. LoadImageFile()

        btn1 = wx.Button(self, label="1.1 Load Image File ")
        btn1.Bind(wx.EVT_BUTTON, LoadImage)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Separation(event):
            self.ColorSeparation()

        btn2 = wx.Button(self, label="1.2 Color Separation ")
        btn2.Bind(wx.EVT_BUTTON, Separation)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def Transformation(event):
            self.ColorTransformation()

        corner_detection = wx.Button(self, label="1.3 Color Transformation ")
        corner_detection.Bind(wx.EVT_BUTTON, Transformation)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Blend(event):
            self.Blending()

        corner_detection = wx.Button(self, label="1.4 Blending ")
        corner_detection.Bind(wx.EVT_BUTTON, Blend)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def LoadImageFile(self):
        img = cv2.imread('Dataset_OpenCvDl_Hw1/Q1_Image/Sun.jpg')
        h, w = img.shape[:2]
        print('Height : ' + str(h))
        print('Width : ' + str(w))
        cv2.imshow('1.1 Load Image File', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

    def ColorSeparation(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q1_Image/Sun.jpg')
        (imgB, imgG ,imgR) = cv2.split(img)
        imgB = img.copy()
        imgB[:,:,1] = 0
        imgB[:,:,2] = 0
        imgG = img.copy()
        imgG[:,:,0] = 0
        imgG[:,:,2] = 0
        imgR = img.copy()
        imgR[:,:,0] = 0
        imgR[:,:,1] = 0

        img = np.hstack((imgB, imgG, imgR))
        cv2.imshow('1.2 Color Separation', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def ColorTransformation(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q1_Image/Sun.jpg')
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = np.mean(np.asarray(img)/255,axis=2)
        cv2.imshow('1.3 Color Transformation OpenCV function', img1)
        cv2.imshow('1.3 Color Transformation Average weighted', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Blending(self):
        def change(self):
            pos = cv2.getTrackbarPos('Blend','Blend')
            img3 = np.uint8((pos/255)*img1 + (1-pos/255)*img2)
            cv2.imshow('Blend',img3)
            
        img1 = cv2.imread('./Dataset_OpenCvDl_Hw1/Q1_Image/Dog_Weak.jpg', cv2.IMREAD_COLOR)
        img2 = cv2.imread('./Dataset_OpenCvDl_Hw1/Q1_Image/Dog_Strong.jpg', cv2.IMREAD_COLOR)
        cv2.namedWindow('Blend')
        cv2.createTrackbar('Blend','Blend',0,255, change)
        cv2.imshow('Blend',img2)   