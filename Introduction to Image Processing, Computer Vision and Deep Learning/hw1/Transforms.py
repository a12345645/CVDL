import wx
import os
import cv2
import numpy as np

class Transforms(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.imgDict = {}

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="4.Transforms")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Resize(event):
            self.Resize()

        btn1 = wx.Button(self, label="4.1 Resize ")
        btn1.Bind(wx.EVT_BUTTON, Resize)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Translation(event):
            self.Translation()

        btn2 = wx.Button(self, label="4.2 Translation ")
        btn2.Bind(wx.EVT_BUTTON, Translation)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def Angle(event):
            self.Angle()

        corner_detection = wx.Button(self, label="4.3 Rotation, Scaling ")
        corner_detection.Bind(wx.EVT_BUTTON, Angle)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Shearing(event):
            self.Shearing()

        corner_detection = wx.Button(self, label="4.4 Shearing ")
        corner_detection.Bind(wx.EVT_BUTTON, Shearing)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)
    
    def Resize(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q4_Image/SQUARE-01.png')
        image = cv2.resize(img, (256, 256))

        cv2.imshow('Resize', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Translation(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q4_Image/SQUARE-01.png')
        img = cv2.resize(img, (256, 256))

        M = np.float32([[1,0,0],[0,1,60]])

        img = cv2.warpAffine(img, M, (400, 300))

        cv2.imshow('Translation', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

    def Angle(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q4_Image/SQUARE-01.png')
        img = cv2.resize(img, (256, 256))

        H = np.float32([[1,0,0],[0,1,60]])
        img = cv2.warpAffine(img, H, (400, 300))

        M = cv2.getRotationMatrix2D((128, 188), 10, 0.5) 
        img = cv2.warpAffine(img, M, (400, 300))
        cv2.imshow('Angle', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

    def Shearing(self):
        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q4_Image/SQUARE-01.png')
        img = cv2.resize(img, (256, 256))

        H = np.float32([[1,0,0],[0,1,60]])
        img = cv2.warpAffine(img, H, (400, 300))

        M = cv2.getRotationMatrix2D((128, 188), 10, 0.5) 
        img = cv2.warpAffine(img, M, (400, 300))
        
        W = np.float32([[1, 0.5, 0],
                    [0, 1  , 0],
                    [0, 0  , 1]])
        img = cv2.warpPerspective(img, W, (400, 300))
        cv2.imshow('Shearing', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()  