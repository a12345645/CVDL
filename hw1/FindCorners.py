import cv2
import wx
import os

class FindCorners():
    def __init__(self,panel, boxSizer):
        self.panel = panel

        self.boxSizer = boxSizer

        self.boxSizer.Clear(True)
        
        self.folder_address = wx.StaticText(self.panel,label=self.panel.path)
        self.boxSizer.Add(self.folder_address, flag=wx.TOP, border= 15)

        folder_chooser = wx.Button(self.panel, label="choose the folder")
        folder_chooser.Bind(wx.EVT_BUTTON, self.choose_folder)
        self.boxSizer.Add(folder_chooser, flag=wx.LEFT|wx.TOP, border=5)

        start = wx.Button(self.panel, label="start")
        start.Bind(wx.EVT_BUTTON, self.StartCornerDetection)
        self.boxSizer.Add(start, flag=wx.LEFT|wx.TOP, border=5)

        self.imgSizer = wx.BoxSizer(wx.VERTICAL)
        self.boxSizer.Add(self.imgSizer,flag=wx.LEFT|wx.TOP, border=5)

        self.boxSizer.Fit(self.panel)
        self.panel.Fit()




    def choose_folder(self, event):

        folder = wx.DirDialog(self.panel, style=wx.DD_CHANGE_DIR,defaultPath= '',
                                message="choose the folder")

        if folder.ShowModal() == wx.ID_OK:
                folder_path = folder.GetPath()
        folder.Destroy()
        self.folder_address.SetLabel(folder_path)

    def StartCornerDetection(self, event):
        fileDir = self.folder_address.LabelText
        fileExt = (r".jpg", r".bmp", r".png", r'jpeg')
        self.panel.path = [os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]
        
        self.imgSizer.Clear(True)

        for i in self.panel.path:
            
            self.FindChessboard(i)
        self.panel.Fit()
    
    def FindChessboard(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (11,8), None)

        if ret:
            criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            

            cv2.drawChessboardCorners(img, (11,8), corners, ret)
            
            name = path.split('/')[-1].split('\\')[-1]

            start = wx.Button(self.panel, label=name)
            start.img = img
            start.Bind(wx.EVT_BUTTON, self.ShowImg)
            self.imgSizer.Add(start)

            self.imgSizer.Fit(self.panel)
        
    def ShowImg(self, event):
        img = event.GetEventObject().img
        cv2.imshow('chess board', img)
        cv2.waitKey(500)