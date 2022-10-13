#coding=utf-8
import wx
import os
from BackgroundSubtraction import BackgroundSubtraction
from OpticalFlow import OpticalFlow
from PerspectiveTransform  import PerspectiveTransform
from PCA import thePCA

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="2021 cvdl Hw2", size = (400, 300))
    nb = wx.Notebook(frame)
    nb.AddPage(BackgroundSubtraction(nb),"1.Background Subtraction ")
    nb.AddPage(OpticalFlow  (nb),"2.Optical Flow  ")
    nb.AddPage(PerspectiveTransform(nb), "3.Perspective Transform ")
    nb.AddPage(thePCA(nb), "4. PCA")
    frame.Show()
    app.MainLoop()