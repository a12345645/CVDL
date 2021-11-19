#coding=utf-8
import wx
import os
from ImageProcessing import ImageProcessing
from AugmentedReality import AugmentedReality
from StereoDisparityMap import StereoDisparityMap
from SIFT import SIFT

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (400, 300))
    nb = wx.Notebook(frame)
    nb.AddPage(ImageProcessing(nb),"1.Image Processing ")
    nb.AddPage(AugmentedReality(nb),"2.Augmented Reality")
    nb.AddPage(StereoDisparityMap(nb), "3. Stereo Disparity Map")
    nb.AddPage(SIFT(nb), "4. SIFT")
    frame.Show()
    app.MainLoop()