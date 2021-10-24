#coding=utf-8
import wx
import os
from CameraCalibration import CameraCalibration
from AugmentedReality import AugmentedReality
from StereoDisparityMap import StereoDisparityMap

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (1200, 1000))
    nb = wx.Notebook(frame)
    nb.AddPage(CameraCalibration(nb),"1.Camera Calibration")
    nb.AddPage(AugmentedReality(nb),"2.Augmented Reality")
    nb.AddPage(StereoDisparityMap(nb), "3. Stereo Disparity Map")
    frame.Show()
    app.MainLoop()