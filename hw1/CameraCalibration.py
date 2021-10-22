import wx
import os
import cv2
import numpy as np
import pprint

class CameraCalibration(wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="1.Calibration")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def CornerDetection(event):
            self.FindCorners()

        corner_detection = wx.Button(self, label="1.1 Find Corners ")
        corner_detection.Bind(wx.EVT_BUTTON, CornerDetection)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def IntrinsicMatrix(event):
            self.FindIntrinsic()

        corner_detection = wx.Button(self, label="1.2 Find Intrinsic ")
        corner_detection.Bind(wx.EVT_BUTTON, IntrinsicMatrix)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Distortion(event):
            self.FindDistortion()

        corner_detection = wx.Button(self, label="1.4 Find Distortion  ")
        corner_detection.Bind(wx.EVT_BUTTON, Distortion)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)


        boxsizer.Add(wx.CheckBox(self, label="Generate Default Constructor"),
            flag=wx.LEFT, border=5)

        boxsizer.Add(wx.CheckBox(self, label="Generate Main Method"),
            flag=wx.LEFT|wx.BOTTOM, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

        self.lSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.lSizer)

        self.folder_address = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.folder_address, flag=wx.TOP, border= 15)

        folder_chooser = wx.Button(self, label="choose the folder")
        folder_chooser.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.lSizer.Add(folder_chooser, flag=wx.LEFT|wx.TOP, border=5)

        self.ldownSizer = wx.BoxSizer(wx.VERTICAL)
        self.lSizer.Add(self.ldownSizer)

    def FindCorners(self):
        self.ldownSizer.Clear(True)
        self.mode = 1

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ldownSizer.Add(mainSizer,flag=wx.LEFT|wx.TOP, border=5)

        btnSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(btnSizer,flag=wx.LEFT|wx.TOP, border=5)

        showSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(showSizer,flag=wx.LEFT|wx.TOP, border=5)

        def ShowImg(event):
            showSizer.Clear(True)

            img = event.GetEventObject().img
            img_height, img_width = img.shape[:2]
            img_height = int(img_height/ 2)
            img_width = int(img_width/ 2)
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            pic = wx.Bitmap.FromBuffer(img_width, img_height, img)
            
            bmp =  wx.StaticBitmap(self, -1, pic)
            showSizer.Add(bmp)

            showSizer.Fit(self)
            self.Fit()

        for i in self.imgDict.keys():
            btn = wx.Button(self, label=i)
            btn.img = self.imgDict[i]
            btn.Bind(wx.EVT_BUTTON, ShowImg)
            btnSizer.Add(btn)
        self.ldownSizer.Fit(self)
        self.Fit()    

    def FindIntrinsic(self):
        self.ldownSizer.Clear(True)
        self.mode = 2

        self.textBox =wx.TextCtrl(parent = self,style = wx.TE_MULTILINE, size = (400,300))
        self.ldownSizer.Add(self.textBox)

        self.textBox.SetLabel('Intrinsic Matrix :' + pprint.pformat(self.mtx))

        self.ldownSizer.Fit(self)
        self.Fit()

    def FindDistortion(self):
        self.ldownSizer.Clear(True)
        self.mode = 3

        self.textBox =wx.TextCtrl(parent = self,style = wx.TE_MULTILINE, size = (400,300))
        self.ldownSizer.Add(self.textBox)

        self.textBox.SetLabel('distortion Matrix :' + pprint.pformat(self.dist))

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
            self.FindDistortion()

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
        self.imgDict = {}

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

                # Draw and display the corners
                cv2.drawChessboardCorners(img, (11,8), corners2, ret)

                name = fname.split('/')[-1].split('\\')[-1]
                self.imgDict[name] = img

        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
