#coding=utf-8
import wx
import cv2 
import os

from wx.core import BitmapDataObject

class CameraCalibration(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="1.Calibration")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        corner_detection = wx.Button(self, label="1.1 Find Corners ")
        corner_detection.Bind(wx.EVT_BUTTON, self.CornerDetection)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        boxsizer.Add(wx.CheckBox(self, label="Generate Default Constructor"),
            flag=wx.LEFT, border=5)

        boxsizer.Add(wx.CheckBox(self, label="Generate Main Method"),
            flag=wx.LEFT|wx.BOTTOM, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

        self.lSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.lSizer)



    def CornerDetection(self, event):
        self.lSizer.Clear(True)
        
        self.folder_address = wx.StaticText(self,label='')
        self.lSizer.Add(self.folder_address, border = 5)

        folder_chooser = wx.Button(self, label="choose the folder")
        folder_chooser.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.lSizer.Add(folder_chooser)

        start = wx.Button(self, label="start")
        start.Bind(wx.EVT_BUTTON, self.StartCornerDetection)
        self.lSizer.Add(start)

        self.imgSizer = wx.BoxSizer(wx.VERTICAL)
        self.lSizer.Add(self.imgSizer)

        self.lSizer.Fit(self)




    def choose_folder(self, event):

        folder = wx.DirDialog(self, style=wx.DD_CHANGE_DIR,defaultPath= './',
                                message="choose the folder")

        if folder.ShowModal() == wx.ID_OK:
                folder_path = folder.GetPath()
        folder.Destroy()
        self.folder_address.SetLabel(folder_path)

    def StartCornerDetection(self, event):
        fileDir = self.folder_address.LabelText
        fileExt = (r".jpg", r".bmp", r".png", r'jpeg')
        image_path = [os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]
        print (image_path)
        for i in image_path:
            image = cv2.imread(i)
            self.find_chessboard(image)
    
    def find_chessboard(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (6, 6), None)

        # Make sure the chess board pattern was found in the image
        if ret:
            # Refine the corner position
            criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            

            # Draw the corners on the image
            cv2.drawChessboardCorners(img, (6, 6), corners, ret)
        
        # Display the image
            
            bm = self.scaled_bitmap(img, 0.2)
            self.btm = wx.StaticBitmap(self, wx.ID_ANY, bm)
            self.imgSizer.Add(self.btm)
            cv2.imshow('chess board', img)
            cv2.waitKey(500)

    def scaled_bitmap(self, bm, scale):
        (height, width) = bm.shape[:2]
        img = wx.BitmapFromBuffer(width, height, bm)
        return wx.BitmapFromImage(img)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (800, 500))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    frame.Show()
    app.MainLoop()