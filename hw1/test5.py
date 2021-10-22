import wx, wx.lib.scrolledpanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = scrolled_panel = \
            wx.lib.scrolledpanel.ScrolledPanel(parent=self, id=-1)
        scrolled_panel.SetupScrolling()

        text = "Ooga booga\n" * 50
        static_text=wx.StaticText(scrolled_panel, -1, text)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(static_text, wx.EXPAND, 0)

        scrolled_panel.SetSizer(sizer)

        self.Show()

        self.panel.SetFocus()
        scrolled_panel.Bind(wx.EVT_SET_FOCUS, self.onFocus)

    def onFocus(self, event):
        self.panel.SetFocus()

if __name__=="__main__":
    app = wx.PySimpleApp()
    my_frame=MyFrame(None, -1)
    app.MainLoop()