from numpy.core.fromnumeric import shape
import wx
import os
import cv2
import numpy as np
import pprint

from wx.core import EAST

class BackgroundSubtraction(wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        self.path = ''

        self.mode = 0

        self.imgDict = {}

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="1.Background Subtraction")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Background(event):
            self. Subtraction()

        btn1 = wx.Button(self, label="1.1 Background Subtraction ")
        btn1.Bind(wx.EVT_BUTTON, Background)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def Subtraction(self):
        i = mean = std = 0
        frames = []

        capture = cv2.VideoCapture("./Dataset_CvDl_Hw2/Q1_Image/traffic.mp4")
        fps = capture.get(cv2.CAP_PROP_FPS)

        while(capture.isOpened()):

            ret, frame = capture.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mask = np.zeros_like(gray)

            if i < 25:
                frames.append(gray)
            elif i == 25:
                frames.append(gray)
                frames = np.array(frames)
                mean = np.mean(frames, axis=0)
                std = np.std(frames, axis=0)
                std[std < 5] = 5
            else:
                diff = np.subtract(gray, mean)
                diff = np.absolute(diff)
                mask[diff > 5*std] = 255

            result = cv2.bitwise_and(frame, frame, mask = mask)

            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            result = np.hstack((frame, mask, result))
            
            cv2.imshow('1.1 Background Subtraction', result)

            if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                break

            i += 1

        capture.release()
        cv2.destroyAllWindows()
        