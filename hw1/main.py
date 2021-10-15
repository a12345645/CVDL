#coding=utf-8
import wx
import cv2 
import os

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
        start.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.lSizer.Add(start)

        self.lSizer.Fit(self)




    def choose_folder(self, event):

        folder = wx.DirDialog(self, style=wx.DD_CHANGE_DIR,defaultPath= './',
                                message="choose the folder")

        if folder.ShowModal() == wx.ID_OK:
                folder_path = folder.GetPath()
        folder.Destroy()
        self.folder_address.SetLabel(folder_path)

    def StartCornerDetection():
        fileDir = r"C:\Test"
        fileExt = r".txt"
        [os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]
        
    def find_chessboard(frame):
        chessboard_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
        return cv2.findChessboardCorners(chessboard_flags, (9, 6), chessboard_flags)[0] 

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (800, 500))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    frame.Show()
    app.MainLoop()