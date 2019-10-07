import wx

from GUI.window import Window

if __name__ == "__main__":
    app = wx.App()
    frame = Window(
        None,
        title="",
        size=(425, 250),
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    )
    app.MainLoop()
