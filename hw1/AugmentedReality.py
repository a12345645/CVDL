import wx
import os
import cv2
import numpy as np

class AugmentedReality (wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        libpath = './Dataset_CvDl_Hw1/Q2_Image/Q2_lib/'
        onboard = cv2.FileStorage(libpath + "alphabet_lib_onboard.txt", cv2.FILE_STORAGE_READ)
        vertical = cv2.FileStorage(libpath + "alphabet_lib_vertical.txt", cv2.FILE_STORAGE_READ)

        self.img = []
        self.path = ''

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="2.Augmented Reality ")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def OnBoard(event):
            self.ShowWord(onboard)

        self.thetext = wx.TextCtrl(self)
        boxsizer.Add(self.thetext, flag=wx.LEFT|wx.TOP, border= 5)
        
        corner_detection = wx.Button(self, label="2.1 Show Words on Board ")
        corner_detection.Bind(wx.EVT_BUTTON, OnBoard)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        def Vertically(event):
            self.ShowWord(vertical)

        corner_detection = wx.Button(self, label="2.2 Show Words Vertically ")
        corner_detection.Bind(wx.EVT_BUTTON, Vertically)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

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

    def ShowWord(self, alphabetLib):
        if(self.img == []):
            return

        self.ldownSizer.Clear(True)

        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        self.ldownSizer.Add(mainBox)

        left = wx.Button(self, label="<", size = (50,50))
        mainBox.Add(left, wx.CENTER, flag=wx.LEFT|wx.TOP, border=5)

        showImgBox = wx.BoxSizer(wx.HORIZONTAL)
        mainBox.Add(showImgBox, flag=wx.LEFT|wx.TOP, border=5)
        
        right = wx.Button(self, label=">", size = (50,50))
        mainBox.Add(right, wx.CENTER, flag=wx.LEFT|wx.TOP, border=5)

        page = [0]

        def ShowImage(n):
            showImgBox.Clear(True)

            img = self.img[n].copy()
            rvec = self.rvecs[n] # rotation vector
            tvec = self.tvecs[n] # translation vector

            def DrowWord(t, n):
                Word = alphabetLib.getNode(t).mat()

                xpost = (n % 4) * 3
                ypost = int(n / 4) * 3

                for i in Word:
                    src = np.array(i, np.float)
                    src[0][0] += 9 - xpost
                    src[0][1] += 6 - ypost
                    src[1][0] += 9 - xpost
                    src[1][1] += 6 - ypost
                    
                    cameraMatrix = self.mtx

                    result = cv2.projectPoints(src, rvec, tvec, cameraMatrix, None)


                    result = tuple(map(tuple, result[0]))
                    start = tuple(map(int, result[0][0]))
                    end = tuple(map(int, result[1][0]))
                    cv2.line(img, start, end, (0, 255, 0), 5)

            text = str(self.thetext.GetValue())
            text = text.upper()

            count = 0
            for i in text:
                if(i.isalpha()):
                    DrowWord(i, count)
                    count += 1

            img_height, img_width = img.shape[:2]
            img_height = int(img_height/ 3)
            img_width = int(img_width/ 3)
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            pic = wx.Bitmap.FromBuffer(img_width, img_height, img)
                
            bmp =  wx.StaticBitmap(self, -1, pic)
            showImgBox.Add(bmp)

            showImgBox.Fit(self)
            self.Fit()

        
        
        def ClickLeft(event) :
            page[0] = (page[0] + 1) % len(self.img)
            ShowImage(page[0])
        
        def ClickRight(event) :
            page[0] = (page[0] - 1) % len(self.img)
            ShowImage(page[0])


        left.Bind(wx.EVT_BUTTON, ClickLeft)
        right.Bind(wx.EVT_BUTTON, ClickRight)
        ShowImage(page[0])

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
        self.img = []

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
                self.img.append(img)

        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)