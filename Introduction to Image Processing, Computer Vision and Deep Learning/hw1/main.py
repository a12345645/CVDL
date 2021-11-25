#coding=utf-8
import wx
import os
from ImageProcessing import ImageProcessing
from ImageSmoothing import ImageSmoothing
from EdgeDetection  import EdgeDetection
from Transforms import Transforms

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1", size = (400, 300))
    nb = wx.Notebook(frame)
    nb.AddPage(ImageProcessing(nb),"1.Image Processing ")
    nb.AddPage(ImageSmoothing (nb),"2.Image Smoothing ")
    nb.AddPage(EdgeDetection(nb), "3.Edge Detection ")
    nb.AddPage(Transforms(nb), "4. Transforms")
    frame.Show()
    app.MainLoop()