import wx
import os
import cv2
import numpy as np
import pprint

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

        def Distortion(event):
            self.FindDistortion()

        corner_detection = wx.Button(self, label="1.4 Blending ")
        corner_detection.Bind(wx.EVT_BUTTON, Distortion)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Undistorted(event):
            self.ShowResult()

        corner_detection = wx.Button(self, label="1.5 Show the undistorted result ")
        corner_detection.Bind(wx.EVT_BUTTON, Undistorted)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def LoadImageFile(self):

        img = cv2.imread('./Dataset_OpenCvDl_Hw1/Q1_Image/Sun.jpg')
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
        imgB, imgG ,imgR = cv2.split(img)
        img2 = (imgB + imgG + imgR)
        print(img2)
        img2 = np.array(img2)
        img2 = img2 / 3
        img2 = img2.astype(int)
        h, w = img2.shape[:2]
        print('Height : ' + str(h))
        print('Width : ' + str(w))
        print(img2)

        cv2.imshow('1.3 Color Transformation', img1)
        cv2.waitKey(0)
        cv2.imshow('1.3 Color Transformation', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def FindDistortion(self):
        self.ldownSizer.Clear(True)
        self.mode = 4

        self.textBox =wx.TextCtrl(parent = self,style = wx.TE_MULTILINE, size = (400,300))
        self.ldownSizer.Add(self.textBox)

        self.textBox.SetLabel('distortion Matrix :' + pprint.pformat(self.dist))

        self.ldownSizer.Fit(self)
        self.Fit()

    def ShowResult(self):
        self.ldownSizer.Clear(True)
        self.mode = 5

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ldownSizer.Add(mainSizer,flag=wx.LEFT|wx.TOP, border=5)

        btnSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(btnSizer,flag=wx.LEFT|wx.TOP, border=5)

        imgSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(imgSizer,flag=wx.LEFT|wx.TOP, border=5)

        def ShowImg(event):
            img = event.GetEventObject().img

            imgSizer.Clear(True)

            h,  w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
            dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)

            img_height, img_width = dst.shape[:2]
            img_height = int(img_height/ 3)
            img_width = int(img_width/ 3)
            dst = cv2.resize(dst, (img_height, img_width), interpolation=cv2.INTER_AREA)

            dst = cv2.cvtColor(dst,cv2.COLOR_BGR2RGB)

            pic = wx.Bitmap.FromBuffer(img_width, img_height, dst)
            
            bmp =  wx.StaticBitmap(self, -1, pic)
            imgSizer.Add(bmp)

            img_height, img_width = img.shape[:2]
            img_height = int(img_height/ 3)
            img_width = int(img_width/ 3)
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            pic = wx.Bitmap.FromBuffer(img_width, img_height, img)
            
            bmp =  wx.StaticBitmap(self, -1, pic)
            imgSizer.Add(bmp)

            self.ldownSizer.Fit(self)
            self.Fit()


        for i in self.imgDict.keys():
            btn = wx.Button(self, label=i)

            img, _, _, _ = self.imgDict[i]
            btn.img = img.copy()

            btn.Bind(wx.EVT_BUTTON, ShowImg)
            btnSizer.Add(btn)

        self.ldownSizer.Fit(self)
        self.Fit()

    def choose_folder(self, event):

        folder = wx.DirDialog(self, style=wx.DD_CHANGE_DIR,defaultPath= '',
                                message="choose the folder")

        if folder.ShowModal() == wx.ID_OK:
                self.path = folder.GetPath()
        folder.Destroy()
        self.folder_address.SetLabel(self.path)

        self.lSizer.Fit(self)
        self.Fit()

        self.Execute()

        if self.mode == 1:
            self.FindCorners()
        elif self.mode == 2:
            self.FindIntrinsic()
        elif self.mode == 3:
            self.FindExtrinsic()
        elif self.mode == 4:
            self.FindDistortion()
        elif self.mode == 5:
            self.ShowResult()

    def Execute(self):
        fileExt = (r".jpg", r".bmp", r".png", r'jpeg')
        images = [os.path.join(self.path, _) for _ in os.listdir(self.path) if _.endswith(fileExt)]

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((8*11,3), np.float32)
        objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        
        index = 0

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (11,8), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)

                name = fname.split('/')[-1].split('\\')[-1]
                self.imgDict[name] = (img, corners2, ret, index)
                index += 1

        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
