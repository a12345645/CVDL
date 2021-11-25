import wx
import os
import cv2
import numpy as np

class ImageSmoothing (wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.imgDict = {}

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="2.Image Smoothing")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Gaussian(event):
            self. GaussianBlur()

        btn1 = wx.Button(self, label="2.1 Gaussian Blur ")
        btn1.Bind(wx.EVT_BUTTON, Gaussian)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Bilateral(event):
            self.BilateralFilter()

        btn2 = wx.Button(self, label="2.2 Bilateral Filter ")
        btn2.Bind(wx.EVT_BUTTON, Bilateral)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def Median(event):
            self.MedianFilter()

        corner_detection = wx.Button(self, label="2.3 Median Filter ")
        corner_detection.Bind(wx.EVT_BUTTON, Median)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def GaussianBlur(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q2_Image/Lenna_whiteNoise.jpg')

        img2 = cv2.GaussianBlur(img,(5,5),5)

        cv2.imshow('2.2 Gaussian Blur',img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def BilateralFilter(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q2_Image/Lenna_whiteNoise.jpg')

        img2 = cv2.bilateralFilter(img,9,90,90)

        cv2.imshow('2.3 Bilateral Filter',img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def MedianFilter(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q2_Image/Lenna_pepperSalt.jpg')

        img2 = cv2.medianBlur(img,3)
        img3 = cv2.medianBlur(img,5)

        cv2.imshow('2.3 Median Filter 3x3',img2)
        cv2.imshow('2.3 Median Filter 5x5',img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()