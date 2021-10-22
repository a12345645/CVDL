#coding=utf-8
import wx, wx.lib.scrolledpanel
import cv2 
import os
from FindCorners import FindCorners

class CameraCalibration(wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="1.Calibration")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        corner_detection = wx.Button(self, label="1.1 Find Corners ")
        corner_detection.Bind(wx.EVT_BUTTON, self.CornerDetection)
        boxsizer.Add(corner_detection, flag=wx.LEFT|wx.TOP, border=5)

        corner_detection = wx.Button(self, label="1.2 Find Intrinsic ")
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
        FindCorners(self, self.lSizer)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (800, 500))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    frame.Show()
    app.MainLoop()