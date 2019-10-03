import wx

from GUI.window import Window


def prep():
    # Registering custom events

    pass


if __name__ == "__main__":
    app = wx.App()
    prep()
    frame = Window(None, title="")
    app.MainLoop()

# from notification.notification import notify
# from music.driver import Driver
# from sys import exit
#
# m_driver = Driver()
# user = m_driver.login()
# notify("hello", "test", user or "some test message", sound=True)
# m_driver.out()
# exit(1)
