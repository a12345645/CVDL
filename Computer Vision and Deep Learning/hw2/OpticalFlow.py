import wx
import os
import cv2
import numpy as np

class OpticalFlow (wx.Panel):

    params = cv2.SimpleBlobDetector_Params()
        
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        self.params.minThreshold = 10
        self.params.maxThreshold = 200
        self.params.filterByArea = True
        self.params.minArea = 35
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.8
        self.params.maxCircularity = 0.9
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="2.Optical Flow")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Preprocessing(event):
            self. Preprocessing()

        btn1 = wx.Button(self, label="2.1 Preprocessing ")
        btn1.Bind(wx.EVT_BUTTON, Preprocessing)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Bilateral(event):
            self.BilateralFilter()

        btn2 = wx.Button(self, label="2.2 Bilateral Filter ")
        btn2.Bind(wx.EVT_BUTTON, Bilateral)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def Preprocessing(self):
        
        detector = cv2.SimpleBlobDetector_create(self.params)

        cap = cv2.VideoCapture('./Dataset_CvDl_Hw2/Q2_Image/optical_flow.mp4')
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints = detector.detect(gray)

        for kp in keypoints:
            x, y = map(lambda x: int(x), kp.pt)
            
            frame = cv2.rectangle(frame, (x - 6, y - 6), (x + 6, y + 6), (0, 0, 255), 1)
            frame = cv2.line(frame, (x, y - 6), (x, y + 6), (0, 0, 255), 1)
            frame = cv2.line(frame, (x - 6, y), (x + 6, y), (0, 0, 255), 1)

        cv2.imshow('2.1 Preprocessing', frame)
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()

    def BilateralFilter(self):
        lk_params = dict(
            winSize = (15,15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        detector = cv2.SimpleBlobDetector_create(self.params)


        capture = cv2.VideoCapture('./Dataset_CvDl_Hw2/Q2_Image/optical_flow.mp4')
        fps = capture.get(cv2.CAP_PROP_FPS)

        ret, frame = capture.read()
        gray_1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints = detector.detect(gray_1)

        p0 = np.array([[[kp.pt[0], kp.pt[1]]] for kp in keypoints]).astype(np.float32)
        mask = np.zeros_like(frame)

        while(capture.isOpened()):

            ret, frame = capture.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            p1, st, _ = cv2.calcOpticalFlowPyrLK(gray_1, gray, p0, None, **lk_params)

            good_new = p1[st==1]
            good_old = p0[st==1]


            for i,(new,old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()

                mask = cv2.line(mask, (a, b), (c, d), (0, 255, 255), 2)
                mask = cv2.circle(mask, (a, b), 3, (0, 255, 255), -1)
                frame = cv2.circle(frame, (a, b), 3, (0, 255, 255), -1)
                
            result = cv2.add(frame, mask)
            

            cv2.imshow('2.2 Video tracking', result)
            if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                break

            gray_1 = gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        capture.release()
        cv2.destroyAllWindows()