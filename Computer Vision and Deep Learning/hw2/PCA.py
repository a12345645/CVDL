import wx
import cv2
import numpy as np
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

class thePCA(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL) 
        self.SetSizer(self.mainbox)

        self.rSizer = wx.GridBagSizer(5, 5)
        self.mainbox.Add(self.rSizer)

        sb = wx.StaticBox(self, label="4.PCA")
        
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        def  Reconstruction(event):
            self.Reconstruction()

        btn1 = wx.Button(self, label="4.1 Image Reconstruction ")
        btn1.Bind(wx.EVT_BUTTON, Reconstruction)
        boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)

        def Compute(event):
            self.Compute()

        btn2 = wx.Button(self, label="4.2 Compute the reconstruction error ")
        btn2.Bind(wx.EVT_BUTTON, Compute)
        boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)



        self.rSizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=5)
    
    def Reconstruction(self):
        fig = plt.figure(figsize=(15, 4))
        for id in range(1, 16):

            img = cv2.imread('./Dataset_CvDl_Hw2/Q4_Image/'+str(id)+'.jpg')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            n_img = self.reconstruction(img)
 
            plt.subplot(4, 15, id)
            plt.axis('off')
            plt.imshow(img)

            plt.subplot(4, 15, id + 15)
            plt.axis('off')
            plt.imshow(n_img)

        for id in range(16, 31):
            img = cv2.imread('./Dataset_CvDl_Hw2/Q4_Image/'+str(id)+'.jpg')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            n_img = self.reconstruction(img)

            plt.subplot(4, 15, id + 15)
            plt.axis('off')
            plt.imshow(img)

            plt.subplot(4, 15, id + 30)
            plt.axis('off')
            plt.imshow(n_img)

        fig.text(0, 0.9, 'Original', va='center', rotation='vertical')
        fig.text(0, 0.65, 'Reconstruction', va='center', rotation='vertical')
        fig.text(0, 0.4, 'Original', va='center', rotation='vertical')
        fig.text(0, 0.15, 'Reconstruction', va='center', rotation='vertical')
        plt.tight_layout(pad=0.5)

        plt.show()

    def reconstruction(self, img):
        b, g, r = cv2.split(img)

        pca = PCA(n_components=10)

        lower_dimension_b = pca.fit_transform(b)
        approximation_b = pca.inverse_transform(lower_dimension_b)

        lower_dimension_g = pca.fit_transform(g)
        approximation_g = pca.inverse_transform(lower_dimension_g)

        lower_dimension_r = pca.fit_transform(r)
        approximation_r = pca.inverse_transform(lower_dimension_r)
        
        clip_b = np.clip(approximation_b, a_min = 0, a_max = 255)
        clip_g = np.clip(approximation_g, a_min = 0, a_max = 255)
        clip_r = np.clip(approximation_r, a_min = 0, a_max = 255)
        n_img = (cv2.merge([clip_b, clip_g, clip_r])).astype(np.uint8)
        return n_img

    def Compute(self):
        errorList = []
        for id in range(1, 31):
            img = cv2.imread('./Dataset_CvDl_Hw2/Q4_Image/' + str(id) + '.jpg')
            n_img = self.reconstruction(img)

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            n_img_gray = cv2.cvtColor(n_img, cv2.COLOR_BGR2GRAY)
            n_img_gray = cv2.normalize(n_img_gray, None, 0, 255, cv2.NORM_MINMAX)
            error = np.sum(np.absolute(img_gray-n_img_gray))
            errorList.append(error)
        print(errorList)