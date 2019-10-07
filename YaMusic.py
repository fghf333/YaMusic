import wx

from GUI.window import Window

if __name__ == "__main__":
    app = wx.App()
    frame = Window(None, title="")
    app.MainLoop()
