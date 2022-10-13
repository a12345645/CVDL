import wx
import cv2
import numpy as np
import cv2.aruco as aruco

class PerspectiveTransform (wx.Panel):

    
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="3.Perspective Transform")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Perspective(event):
            self. Transform()

        btn1 = wx.Button(self, label="3.1 Perspective Transform ")
        btn1.Bind(wx.EVT_BUTTON, Perspective)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        
        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)

    def Transform(self):

        logo = cv2.imread("./Dataset_CvDl_Hw2/Q3_Image/logo.png")
        pts_src = np.array([[0, 0], [logo.shape[1], 0], [logo.shape[1], 
                            logo.shape[0]],  [0, logo.shape[0]]], dtype=float)


        capture = cv2.VideoCapture('./Dataset_CvDl_Hw2/Q3_Image/perspective_transform.mp4')
        fps = capture.get(cv2.CAP_PROP_FPS)

        ret, frame = capture.read()

        while(capture.isOpened()):

            ret, frame = capture.read()
            if not ret:
                break

            dictionary = aruco.Dictionary_get(aruco.DICT_4X4_250)
            
            param = aruco.DetectorParameters_create()
            
            markerCornaers, markerIds, rejectedCandidates = aruco.detectMarkers(
                frame,
                dictionary,
                parameters = param
            )
            id1 = np.squeeze(np.where(markerIds == 1))
            id2= np.squeeze(np.where(markerIds == 2))
            id3 = np.squeeze(np.where(markerIds == 3))
            id4 = np.squeeze(np.where(markerIds == 4))

            if id1 != [] and id2 != [] and id3 != [] and id4 != []:
                pt1 = np.squeeze(markerCornaers[id1[0]])[0]
                pt2 = np.squeeze(markerCornaers[id2[0]])[1]
                pt3 = np.squeeze(markerCornaers[id3[0]])[2]
                pt4 = np.squeeze(markerCornaers[id4[0]])[3]

                pts_dst = [[pt1[0], pt1[1]]]
                pts_dst = pts_dst + [[pt2[0], pt2[1]]]
                pts_dst = pts_dst + [[pt3[0], pt3[1]]]
                pts_dst = pts_dst + [[pt4[0], pt4[1]]]
                pts_dst = np.array(pts_dst)

                im_dst = frame
                h, status = cv2.findHomography(pts_src, pts_dst)
                temp = cv2.warpPerspective(logo, h, (im_dst.shape[1], im_dst.shape[0]))
                
                cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)
                im_dst = im_dst + temp
                cv2.imshow('3.1 Perspective Transform', im_dst)
            
            if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                break
        
        capture.release()
        cv2.destroyAllWindows()
    