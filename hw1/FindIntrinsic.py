import cv2
import wx
import os
import numpy as np
import pprint

class FindIntrinsic():
    def __init__(self,panel, boxSizer):
        self.panel = panel

        self.boxSizer = boxSizer

        self.boxSizer.Clear(True)

        self.folder_address = wx.StaticText(self.panel,label=self.panel.path)
        self.boxSizer.Add(self.folder_address, flag=wx.TOP, border= 15)

        folder_chooser = wx.Button(self.panel, label="choose the folder")
        folder_chooser.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.boxSizer.Add(folder_chooser, flag=wx.LEFT|wx.TOP, border=5)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.boxSizer.Add(mainSizer,flag=wx.LEFT|wx.TOP, border=5)

        self.showSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.showSizer,flag=wx.LEFT|wx.TOP, border=5)

        self.boxSizer.Fit(self.panel)
        self.panel.Fit()

        if self.panel.path != '':
            self.Show()



    def choose_folder(self, event):

        folder = wx.DirDialog(self.panel, style=wx.DD_CHANGE_DIR,defaultPath= '',
                                message="choose the folder")

        if folder.ShowModal() == wx.ID_OK:
                self.panel.path = folder.GetPath()
        folder.Destroy()
        self.folder_address.SetLabel(self.panel.path)
        self.Show()

    def Show(self):
        fileExt = (r".jpg", r".bmp", r".png", r'jpeg')
        images = [os.path.join(self.panel.path, _) for _ in os.listdir(self.panel.path) if _.endswith(fileExt)]

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((8*11,3), np.float32)
        objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

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

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        print(ret, mtx, dist, rvecs, tvecs)

        self.textBox =wx.TextCtrl(parent = self.panel,style = wx.TE_MULTILINE, size = (400,300))
        self.showSizer.Add(self.textBox)

        self.textBox.SetLabel('Intrinsic Matrix :' + pprint.pformat(mtx))

        self.showSizer.Fit(self.panel)
        self.panel.Fit()


