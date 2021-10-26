import wx
import os
import cv2

class SIFT(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        self.path = ''

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="3.Stereo Disparity Map ")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def Keyp(event):
            self.Keypoints()

        
        btn1 = wx.Button(self, label="4.1 Keypoints ")
        btn1.Bind(wx.EVT_BUTTON, Keyp)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Matched(event):
            self.MatchedKeypoints()

        btn2 = wx.Button(self, label="4.2 Matched Keypoints ")
        btn2.Bind(wx.EVT_BUTTON, Matched)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        def Warp(event):
            self. WarpImages()

        btn3 = wx.Button(self, label="4.3 Warp Images ")
        btn3.Bind(wx.EVT_BUTTON, Warp)
        boxsizer.Add(btn3, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

        self.lSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainbox.Add(self.lSizer)

        imLtext = wx.StaticText(self,label='imL path')
        self.lSizer.Add(imLtext, flag=wx.TOP, border= 15)

        self.imLtext = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.imLtext)

        def imLbtnClick(event):
            self.choose_filer(self.imLtext)

        imLbtn = wx.Button(self, label="choose the file")
        imLbtn.Bind(wx.EVT_BUTTON, imLbtnClick)
        self.lSizer.Add(imLbtn, flag=wx.LEFT|wx.TOP, border=5)

        imRtext = wx.StaticText(self,label='imR path')
        self.lSizer.Add(imRtext, flag=wx.TOP, border= 5)

        self.imRtext = wx.StaticText(self,label=self.path)
        self.lSizer.Add(self.imRtext)

        def imRbtnClick(event):
            self.choose_filer(self.imRtext)

        imRbtn = wx.Button(self, label="choose the file")
        imRbtn.Bind(wx.EVT_BUTTON, imRbtnClick)
        self.lSizer.Add(imRbtn, flag=wx.LEFT|wx.TOP, border=5)

        self.ldownSizer = wx.BoxSizer(wx.VERTICAL)
        self.lSizer.Add(self.ldownSizer)