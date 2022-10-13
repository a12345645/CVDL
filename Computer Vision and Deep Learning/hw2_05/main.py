import wx
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pickle
import keras
from Resnet50 import Resnet50
import Resnet50 as resnet50 

import cv2

from PIL import Image

from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input

# tensorboard --logdir=logs\20211219-122913

model = Resnet50().model()


def ShowModelStructure(event):
    print(model.summary())
    


def TensorBoard(event):

    print("tensorboard --logdir=logs\\20211219-122913")


# _, _, test_generator = resnet50.data_generator()
test_generator = resnet50.data_generator()

def Test(event):
    
    if(text.GetValue() == ''):
        return
    n = int(text.GetValue())

    model2 = keras.models.load_model('model_46.h5')

    data, label = test_generator[n]
    predict = model2.predict(data)
    print(predict, label)
    if predict < 0.5:
        predict = 0
    else:
        predict = 1

    labels = ['cat', 'dog']

    img = (data[0] * 255).astype('uint8')

    plt.xticks([])
    plt.yticks([])

    plt.title('Class: '+labels[predict])
    plt.imshow(img)

    plt.show()

def Erasing(event):
    lebal = ['none Random-Erasing', 'Random-Erasing']
    acc = [0.935, 0.963]
    x = np.arange(len(acc))
    plt.bar(x, acc, width= 0.2)
    plt.ylim([0.9, 1])
    plt.xticks(x, lebal )
    plt.show()

if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw2_05", size = (500, 500))

    panel = wx.Panel(frame)

    mainbox = wx.BoxSizer(wx.HORIZONTAL) 
    panel.SetSizer(mainbox)

    sb = wx.StaticBox(panel, label="5.Dogs and Cats classification Using ResNet50")    
    boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
    mainbox.Add(boxsizer)
        
    btn1 = wx.Button(panel, label="5.1 Show Model Structure ")
    btn1.Bind(wx.EVT_BUTTON, ShowModelStructure)
    boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)
    
    btn2 = wx.Button(panel, label="5.2 Show TensorBoard ")
    btn2.Bind(wx.EVT_BUTTON, TensorBoard)
    boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)


    btn5 = wx.Button(panel, label="5.3 Test ")
    btn5.Bind(wx.EVT_BUTTON, Test)
    boxsizer.Add(btn5, flag=wx.LEFT|wx.TOP, border=5)

    text = wx.TextCtrl(panel)
    boxsizer.Add(text, flag=wx.LEFT|wx.TOP, border= 5)


    btn4 = wx.Button(panel, label="5.4 Random-Erasing ")
    btn4.Bind(wx.EVT_BUTTON, Erasing)
    boxsizer.Add(btn4, flag=wx.LEFT|wx.TOP, border=5)

    

    leftSizer = wx.BoxSizer(wx.VERTICAL) 
    mainbox.Add(leftSizer)

    panel.Fit()
    frame.Show()
    app.MainLoop()