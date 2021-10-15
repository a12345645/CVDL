#coding=utf-8

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'测试面板Panel', size = (400, 300))
    
        #创建面板
        panel = wx.Panel(self) 
        #创建open，save按钮
        self.bt_open = wx.Button(panel,label='open')
        self.bt_save = wx.Button(panel,label='save')
        #创建文本，左对齐，注意这里style=wx.TE_LEFT，不是wx.ALIGN_LEFT ，表示控件中的输入光标是靠左对齐。
        self.st_tips = wx.StaticText(panel ,0,u"请输入文件路径",style=wx.TE_LEFT )
        self.st_tips2 = wx.StaticText(panel ,0,u"文件路径:",style=wx.TE_LEFT )
        self.text_filename = wx.TextCtrl(panel,style=wx.TE_LEFT)
        #创建文本内容框，多行，垂直滚动条
        self.text_contents = wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.HSCROLL)
    
        #添加容器，容器中控件按横向并排排列
        bsizer_top = wx.BoxSizer(wx.VERTICAL)
        #添加容器，容器中控件按纵向并排排列
        bsizer_center = wx.BoxSizer(wx.HORIZONTAL)
        bsizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        #在容器中添加st_tips控件，proportion=0 代表当容器大小变化时，st_tips控件的大小不变
        #flag = wx.EXPAND|wx.ALL中，wx.ALL代表在st_tips控件四周都增加宽度为x的空白，x取border参数的值，本例是border=5
        # wx.EXPAND代表st_tips控件占满可用空间。
        bsizer_top.Add(self.st_tips,proportion=0,flag=wx.EXPAND|wx.ALL, border = 5 )
        #proportion=1 代表当容器大小变化时，st_tips2控件的大小变化，变化速度为1
        bsizer_center.Add(self.st_tips2,proportion=0,flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT,border = 5 )
        #proportion=2 代表当容器大小变化时，text_filename控件的大小变化，变化速度为2
        bsizer_center.Add(self.text_filename,proportion=2,flag=wx.EXPAND|wx.ALL,border=5)
        bsizer_center.Add(self.bt_open,proportion=1,flag=wx.ALL,border=5)
        bsizer_center.Add(self.bt_save,proportion=0,flag=wx.ALL,border=5)
        
        bsizer_bottom.Add(self.text_contents,proportion=1 ,flag = wx.EXPAND|wx.ALL,border =5 )
        
        #wx.VERTICAL 横向分割
        bsizer_all = wx.BoxSizer(wx.VERTICAL)
        #添加顶部sizer，proportion=0 代表bsizer_top大小不可变化
        bsizer_all.Add(bsizer_top,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        bsizer_all.Add(bsizer_center,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        #添加顶部sizer，proportion=1 代表bsizer_bottom大小变化
        bsizer_all.Add(bsizer_bottom,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        self.Bind(wx.EVT_BUTTON,self.onOpen,self.bt_open)
        #self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
    
        panel.SetSizer(bsizer_all)


    def onOpen(self,event): 
        self.text_contents.AppendText(str(self.GetSizeTuple()))
        self.text_contents.AppendText(str(self.bt_open.GetSizeTuple()))
        self.text_contents.AppendText(str(self.text_filename.GetSizeTuple()))
        self.SetSize((700,600))
        self.text_contents.AppendText(str(self.GetSizeTuple()))
        self.text_contents.AppendText(str(self.bt_open.GetSizeTuple()))
        self.text_contents.AppendText(str(self.text_filename.GetSizeTuple()))        


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(parent = None, id = -1)
    frame.Show()
    frame.Center()
    app.MainLoop()