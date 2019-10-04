import wx
from yandex_music.exceptions import BadRequest

from GUI.builders import Builders
from configs.configs import Configs
from music.API import YandexAPI


class Login(object):
    def __init__(self, parent):
        self.builders = Builders()
        self.conf = Configs()
        self.parent = parent
        self.api = YandexAPI()
        self.validation_error = wx.StaticText()
        self.sizer = wx.BoxSizer()
        self.dialog = wx.Dialog()
        pass

    def create_login_popup(self):
        self.dialog = dialog = wx.Dialog(self.parent, wx.ID_ANY, "", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                                         name="login_popup")
        self.sizer = sizer = wx.BoxSizer(wx.VERTICAL)
        dialog.BackgroundColour = self.conf.get_attr("BACKGROUND_COLOR")

        text = self.builders.static_text_builder(dialog, label="Please login")

        font = text.GetFont()
        font.PointSize += 10
        font = font.Bold()
        text.SetFont(font)

        login_label = self.builders.static_text_builder(dialog, label="Login:")
        login_input = self.builders.input_builder(dialog, name="login_input")

        password_label = self.builders.static_text_builder(dialog, label="Password:")
        password_input = self.builders.input_builder(dialog, name="password_input")

        login_button = self.builders.button_builder(dialog, "Login", "login_button")
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        self.validation_error = self.builders.static_text_builder(dialog, label="")
        self.validation_error.SetForegroundColour(wx.RED)

        sizer.Add(
            text,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            20
        )

        sizer.Add(
            login_label,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            5
        )

        sizer.Add(
            login_input,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        sizer.Add(
            password_label,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            5
        )

        sizer.Add(
            password_input,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        sizer.Add(
            login_button,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        self.sizer.Add(
            self.validation_error,
            1,
            wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,
            5
        )

        dialog.SetSizer(sizer)
        dialog.Bind(wx.EVT_CLOSE, self.on_popup_close)
        dialog.Center()
        dialog.Show()

    def on_popup_close(self, event):
        if self.api.is_logged_in() is True:
            event.Skip(True)
        else:
            self.parent.Close(True)

    def on_login(self, event):
        login_button = self.parent.FindWindowByName("login_button")
        login_button.Disable()
        login = self.parent.FindWindowByName("login_input").GetValue()
        password = self.parent.FindWindowByName("password_input").GetValue()
        try:
            self.api.login(login=login, password=password)
            popup = self.parent.FindWindowByName("login_popup")
            popup.Destroy()
            self.parent.st.SetLabel("Hello " + self.api.get_display_name())
            self.parent.playlist_selection.Enable(True)
            self.parent.make_menu()
        except BadRequest as e:
            self.validation_error.SetLabel(str(e))
            size = self.dialog.GetSize()
            self.dialog.SetInitialSize()
            self.dialog.SetSize(size)
            login_button.Enable()
            event.Skip()


    def on_logout_menu(self, event):
        self.api.logout()
        self.parent.st.SetLabel("Hello None")
        self.create_login_popup()
        self.parent.make_menu()
