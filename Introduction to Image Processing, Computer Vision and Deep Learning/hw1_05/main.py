import wx
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pickle
import keras

from VGG16 import VGG16

class Cifar10():
    trainloader = None
    testloader = None
    classes = ('plane', 'car', 'bird', 'cat',
                 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    def __init__(self) -> None:
        
        file = './data/cifar-10-batches-py/data_batch_1'
        with open(file, 'rb') as fo:
            self.dict = pickle.load(fo, encoding='bytes')

        file = './data/cifar-10-batches-py/test_batch'
        with open(file, 'rb') as fo:
            self.test = pickle.load(fo, encoding='bytes')

    def DataLen(self):
        return len(self.dict[b'data'])

    def ShowImg(self, i, j):

        img = self.dict[b'data'][i:j]
        labels = self.dict[b'labels'][i:j]

        for i in range(9):
            img_flat = img[i]
            img_R = img_flat[0:1024].reshape((32, 32))
            img_G = img_flat[1024:2048].reshape((32, 32))
            img_B = img_flat[2048:3072].reshape((32, 32))
            imgs = np.dstack((img_R, img_G, img_B))
            plt.subplot(3, 3, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.title(self.classes[labels[i]])
            plt.imshow(imgs)

        plt.show()

    def GetTrainData(self):
        data = []
        for i in self.dict[b'data']:
            img_flat = i
            img_R = img_flat[0:1024].reshape((32, 32))
            img_G = img_flat[1024:2048].reshape((32, 32))
            img_B = img_flat[2048:3072].reshape((32, 32))
            imgs = np.dstack((img_R, img_G, img_B))
            data.append(imgs)

        label = tf.cast(self.dict[b'labels'], dtype=tf.int32)
        label = tf.squeeze(label)
        label = tf.one_hot(label, depth=10)

        return np.array(data), label

    def GetTest(self, n):
        img_flat = self.test[b'data'][n]
        label = self.test[b'labels'][n]

        img_R = img_flat[0:1024].reshape((32, 32))
        img_G = img_flat[1024:2048].reshape((32, 32))
        img_B = img_flat[2048:3072].reshape((32, 32))
        img = np.dstack((img_R, img_G, img_B))
        return img, self.classes[label]


cifar10 = Cifar10()
vgg16 = VGG16()

def ShowImages(event):
    leftSizer.Clear()
    dataLen = cifar10.DataLen()
    cifar10.ShowImg(0, 9)
    

def ShowHyperparameters(event):
    vgg16.printOptimizer()

def ShowModel(event):
    print(vgg16.model.summary())

def ShowAccuracyLoss(event):

    img_array=plt.imread("accuracy.png") 
    plt.subplot(1, 2, 1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img_array)

    img_array=plt.imread("loss.png") 
    plt.subplot(1, 2, 2)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img_array)

    plt.show()


def Test(event):
    plt.clf()
    
    model = keras.models.load_model('model.h5')

    if(text.GetValue() == ''):
        return
    n = int(text.GetValue())
    img, label = cifar10.GetTest(n + 1)

    predict = model.predict(np.array([img]))[0]

    plt.subplot(1, 2, 1)
    plt.xticks([])
    plt.yticks([])
    plt.title(label)
    plt.imshow(img)

    x = np.arange(len(predict))

    plt.subplot(1, 2, 2)
    plt.bar(x, predict)

    plt.xticks(x, list(cifar10.classes))
    plt.show()


if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None, title="2021 Opencvdl Hw1_05", size = (500, 500))

    panel = wx.Panel(frame)

    mainbox = wx.BoxSizer(wx.HORIZONTAL) 
    panel.SetSizer(mainbox)

    sb = wx.StaticBox(panel, label="1.Training Cifar10 Classifier Using VGG16")    
    boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
    mainbox.Add(boxsizer)
        
    btn1 = wx.Button(panel, label="5.1 Show Training Images ")
    btn1.Bind(wx.EVT_BUTTON, ShowImages)
    boxsizer.Add(btn1, flag=wx.LEFT|wx.TOP, border=5)
    
    btn2 = wx.Button(panel, label="5.2 Show Hyperparameters ")
    btn2.Bind(wx.EVT_BUTTON, ShowHyperparameters)
    boxsizer.Add(btn2, flag=wx.LEFT|wx.TOP, border=5)

    btn3 = wx.Button(panel, label="5.3 Show Model Structure ")
    btn3.Bind(wx.EVT_BUTTON, ShowModel)
    boxsizer.Add(btn3, flag=wx.LEFT|wx.TOP, border=5)

    btn4 = wx.Button(panel, label="5.4 Show Accuracy and Loss ")
    btn4.Bind(wx.EVT_BUTTON, ShowAccuracyLoss)
    boxsizer.Add(btn4, flag=wx.LEFT|wx.TOP, border=5)

    text = wx.TextCtrl(panel)
    boxsizer.Add(text, flag=wx.LEFT|wx.TOP, border= 5)

    btn5 = wx.Button(panel, label="5.5 Test ")
    btn5.Bind(wx.EVT_BUTTON, Test)
    boxsizer.Add(btn5, flag=wx.LEFT|wx.TOP, border=5)

    leftSizer = wx.BoxSizer(wx.VERTICAL) 
    mainbox.Add(leftSizer)

    panel.Fit()
    frame.Show()
    app.MainLoop()