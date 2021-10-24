#coding=utf-8
import wx
import os
from CameraCalibration import CameraCalibration
from AugmentedReality import AugmentedReality

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (1000, 800))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    nb.AddPage(AugmentedReality(nb),"2.Augmented Reality")
    frame.Show()
    app.MainLoop()