import wx
import os
import cv2
import numpy as np

class SIFT(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        self.path = ''

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="3.Stereo Disparity Map ")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def Keyp(event):
            self.Keypoints()
        
        btn1 = wx.Button(self, label="4.1 Keypoints ")
        btn1.Bind(wx.EVT_BUTTON, Keyp)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Matched(event):
            self.MatchedKeypoints()

        btn2 = wx.Button(self, label="4.2 Matched Keypoints ")
        btn2.Bind(wx.EVT_BUTTON, Matched)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def Warp(event):
            self. WarpImages()

        btn3 = wx.Button(self, label="4.3 Warp Images ")
        btn3.Bind(wx.EVT_BUTTON, Warp)
        boxsizer.Add(btn3, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

        self.lSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.lSizer)

        imLtext = wx.StaticText(self,label='image1 path')
        self.lSizer.Add(imLtext, flag=wx.TOP, border= 15)

        self.image1 = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.image1)

        def imLbtnClick(event):
            self.choose_filer(self.image1)

        imLbtn = wx.Button(self, label="choose the file")
        imLbtn.Bind(wx.EVT_BUTTON, imLbtnClick)
        self.lSizer.Add(imLbtn, flag=wx.LEFT|wx.TOP, border=5)

        imRtext = wx.StaticText(self,label='image2 path')
        self.lSizer.Add(imRtext, flag=wx.TOP, border= 5)

        self.image2 = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.image2)

        def imRbtnClick(event):
            self.choose_filer(self.image2)

        imRbtn = wx.Button(self, label="choose the file")
        imRbtn.Bind(wx.EVT_BUTTON, imRbtnClick)
        self.lSizer.Add(imRbtn, flag=wx.LEFT|wx.TOP, border=5)

        self.ldownSizer = wx.BoxSizer(wx.VERTICAL)
        self.lSizer.Add(self.ldownSizer)

    def ROOTSIFT(self, grayIMG, kpsData):
        extractor = cv2.DescriptorExtractor_create('SIFT')
        (kps, descs) = extractor.compute(grayIMG, kpsData)

        if len(kps) > 0:
            #L1-正規化
            eps=1e-7
            descs /= (descs.sum(axis=1, keepdims=True) + eps)
            #取平方根
            descs = np.sqrt(descs)
            return (kps, descs)
        else:
            return ([], None)

    def Keypoints(self):
        path1 = self.image1.GetLabelText()
        path2 = self.image2.GetLabelText()

        if path1 == '' or path2 == '' :
            return
        
        sift = cv2.xfeatures2d.SIFT_create()

        img1 = cv2.imread(path1)
        gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        kp1 = sift.detect(gray,None)

        kp1 = sorted(kp1, key = lambda kp : kp.size,reverse=True)

        if(len(kp1) > 200):
            kp1 = kp1[:200]

        img1=cv2.drawKeypoints(gray,kp1,img1)

        img2 = cv2.imread(path2)
        gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        kp2 = sift.detect(gray,None)

        kp2 = sorted(kp2, key = lambda kp : kp.size,reverse=True)

        if(len(kp2) > 200):
            kp2 = kp2[:200]

        img2=cv2.drawKeypoints(gray,kp2,img1)

        self.ldownSizer.Clear(True)

        Box = wx.BoxSizer(wx.HORIZONTAL)
        self.ldownSizer.Add(Box)

        # img1
        img_height, img_width = img1.shape[:2]
        pic = wx.Bitmap.FromBuffer(img_width, img_height, img1)
        bmp1 =  wx.StaticBitmap(self, -1, pic)
        Box.Add(bmp1)

        # img2
        img_height, img_width = img2.shape[:2]
        pic = wx.Bitmap.FromBuffer(img_width, img_height, img2)
        bmp2 =  wx.StaticBitmap(self, -1, pic)
        Box.Add(bmp2)

        self.ldownSizer.Fit(self)
        self.Fit()

    def MatchedKeypoints(self):
        path1 = self.image1.GetLabelText()
        path2 = self.image2.GetLabelText()

        if path1 == '' or path2 == '' :
            return
        
        sift = cv2.xfeatures2d.SIFT_create()

        img1 = cv2.imread(path1)
        gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        kp1 = sift.detect(gray1,None)

        kp1 = sorted(kp1, key = lambda kp : kp.size,reverse=True)

        if(len(kp1) > 200):
            kp1 = kp1[:200]

        img1=cv2.drawKeypoints(gray1,kp1,img1)

        img2 = cv2.imread(path2)
        gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        kp2 = sift.detect(gray2,None)

        kp2 = sorted(kp2, key = lambda kp : kp.size,reverse=True)

        if(len(kp2) > 200):
            kp2 = kp2[:200]

        img2=cv2.drawKeypoints(gray2,kp2,img1)



        (kpsA, featuresA) = self.ROOTSIFT(gray1, kp1)

        (kpsB, featuresB) = self.ROOTSIFT(gray2, kp2)

        matcher = cv2.DescriptorMatcher_create('BruteForce')
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)

        matches = []
        for m in rawMatches:

            if len(m) == 2 and m[0].distance < m[1].distance * 0.8:

                matches.append((m[0].trainIdx, m[0].queryIdx))

        (hA, wA) = img1.shape[:2]

        (hB, wB) = img2.shape[:2]

        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype='uint8')

        vis[0:hA, 0:wA] = img1

        vis[0:hB, wA:] = img2

        for (trainIdx, queryIdx) in matches:

            color = np.random.randint(0, high=255, size=(3,))

            ptA = (int(kpsA[queryIdx].pt[0]), int(kpsA[queryIdx].pt[1]))

            ptB = (int(kpsB[trainIdx].pt[0] + wA), int(kpsB[trainIdx].pt[1]))

            cv2.line(vis, ptA, ptB, color, 2)

        self.ldownSizer.Clear(True)

        img_height, img_width = vis.shape[:2]
        pic = wx.Bitmap.FromBuffer(img_width, img_height, vis)
        bmp1 =  wx.StaticBitmap(self, -1, pic)
        self.ldownSizer.Add(bmp1)

        self.ldownSizer.Fit(self)
        self.Fit()

    def choose_filer(self, text):

        wildcard = "JPG files (*.jpg)|*.jpg|BMP files (*.bmp)|*.bmp|PNG files (*.png)|*.png"
        filer = wx.FileDialog(self, "Open XYZ file", wildcard=wildcard,
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        path = ''
        if filer.ShowModal() == wx.ID_OK:
                path = filer.GetPath()
        filer.Destroy()
        text.SetLabel(path)

        self.lSizer.Fit(self)
        self.Fit()
    

        