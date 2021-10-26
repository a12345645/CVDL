import wx
import os
import cv2
import numpy as np

class StereoDisparityMap (wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        self.path = ''

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="3.Stereo Disparity Map ")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def Disparity(event):
            self.StereoDisparity()

        
        btn1 = wx.Button(self, label="3.1 Stereo Disparity Map ")
        btn1.Bind(wx.EVT_BUTTON, Disparity)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Checking(event):
            self.Checking()

        btn2 = wx.Button(self, label="3.2 Checking the Disparity Value ")
        btn2.Bind(wx.EVT_BUTTON, Checking)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

        self.lSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.lSizer)

        imLtext = wx.StaticText(self,label='imL path')
        self.lSizer.Add(imLtext, flag=wx.TOP, border= 15)

        self.imLtext = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.imLtext)

        def imLbtnClick(event):
            self.choose_filer(self.imLtext)

        imLbtn = wx.Button(self, label="choose the file")
        imLbtn.Bind(wx.EVT_BUTTON, imLbtnClick)
        self.lSizer.Add(imLbtn, flag=wx.LEFT|wx.TOP, border=5)

        imRtext = wx.StaticText(self,label='imR path')
        self.lSizer.Add(imRtext, flag=wx.TOP, border= 5)

        self.imRtext = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.imRtext)

        def imRbtnClick(event):
            self.choose_filer(self.imRtext)

        imRbtn = wx.Button(self, label="choose the file")
        imRbtn.Bind(wx.EVT_BUTTON, imRbtnClick)
        self.lSizer.Add(imRbtn, flag=wx.LEFT|wx.TOP, border=5)

        self.ldownSizer = wx.BoxSizer(wx.VERTICAL)
        self.lSizer.Add(self.ldownSizer)

    def StereoDisparity(self):
        pathL = self.imLtext.GetLabelText()
        pathR = self.imRtext.GetLabelText()
        #pathL = pathR= './Dataset_CvDl_Hw1/Q2_Image/1.bmp'

        if pathR == '' or pathL == '' :
            return

        imgL = cv2.imread(pathL)
        imgR = cv2.imread(pathR)
        imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
        imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

        def resize(img):
            img_height, img_width = img.shape[:2]
            img_height = img_height - img_height % 256
            img_width = img_width - img_width % 256
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)
            return img

        imgL = resize(imgL)
        imgR = resize(imgR)

        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)

        img = stereo.compute(imgL, imgR)
        img = cv2.normalize(img, img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        self.ldownSizer.Clear(True)

        img_height, img_width = img.shape[:2]

        img_height = int(img_height/ 3)
        img_width = int(img_width/ 3)
        img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) # FromBuffer have BGR
        img_height, img_width = img.shape[:2]

        pic = wx.Bitmap.FromBuffer(img_width, img_height, img)
            
        bmp =  wx.StaticBitmap(self, -1, pic)
        self.ldownSizer.Add(bmp)

        self.ldownSizer.Fit(self)
        self.Fit()
    def Checking(self):
        pathL = self.imLtext.GetLabelText()
        pathR = self.imRtext.GetLabelText()

        if pathR == '' or pathL == '' :
            return

        imgL = cv2.imread(pathL)
        imgR = cv2.imread(pathR)

        def resize(img):
            img_height, img_width = img.shape[:2]
            img_height = img_height - img_height % 256
            img_width = img_width - img_width % 256
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)
            return img

        imgL = resize(imgL)
        imgR = resize(imgR)

        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)

        imgLgray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
        imgRgray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
        disp  = stereo.compute(imgLgray, imgRgray)
        disp = cv2.normalize(disp, disp, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        img_height, img_width = disp.shape[:2]

        img_height = int(img_height/ 4)
        img_width = int(img_width/ 4)
        disp = cv2.resize(disp, (img_height, img_width), interpolation=cv2.INTER_AREA)

        self.ldownSizer.Clear(True)
        Box = wx.BoxSizer(wx.HORIZONTAL)
        self.ldownSizer.Add(Box)

        # imgL
        imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
        img_height, img_width = imgL.shape[:2]

        img_height = int(img_height/ 4)
        img_width = int(img_width/ 4)
        imgLshow = cv2.resize(imgL, (img_height, img_width), interpolation=cv2.INTER_AREA)

        img_height, img_width = imgLshow.shape[:2]

        pic = wx.Bitmap.FromBuffer(img_width, img_height, imgLshow)
            
        bmpL =  wx.StaticBitmap(self, -1, pic)
        Box.Add(bmpL)

        # imgR
        imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)
        img_height, img_width = imgR.shape[:2]

        img_height = int(img_height/ 4)
        img_width = int(img_width/ 4)
        imgRshow = cv2.resize(imgR, (img_height, img_width), interpolation=cv2.INTER_AREA)

        img_height, img_width = imgRshow.shape[:2]

        pic = wx.Bitmap.FromBuffer(img_width, img_height, imgRshow)
            
        bmpR =  wx.StaticBitmap(self, -1, pic)
        Box.Add(bmpR)
        

        def on_clic(event):
            x, y=event.GetPosition()

            dist = int(disp[y][x] / 4)

            img = imgRshow.copy()

            img = cv2.circle(img, (x - dist, y), 5, (0,0,255), 10)

            img_height, img_width = img.shape[:2]

            pic = wx.Bitmap.FromBuffer(img_width, img_height, img)
                
            bmpR.SetBitmap(pic)
            self.ldownSizer.Fit(self)
            self.Fit()


        bmpL.Bind(wx.EVT_LEFT_DOWN, on_clic)

        self.ldownSizer.Fit(self)
        self.Fit()

    def choose_filer(self, text):

        wildcard = "PNG files (*.png)|*.png|BMP files (*.bmp)|*.bmp|JPG files (*.jpg)|*.jpg"
        filer = wx.FileDialog(self, "Open XYZ file", wildcard=wildcard,
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        path = ''
        if filer.ShowModal() == wx.ID_OK:
                path = filer.GetPath()
        filer.Destroy()
        text.SetLabel(path)

        self.lSizer.Fit(self)
        self.Fit()