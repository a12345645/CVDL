#coding=utf-8
import wx
import os
from CameraCalibration import CameraCalibration

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (800, 500))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    frame.Show()
    app.MainLoop()