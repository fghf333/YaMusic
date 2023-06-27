from urllib.parse import urlparse, parse_qs

import wx
import wx.html2 as webview

from GUI.builders import Builders
from configs.configs import Configs
from music.API import YandexAPI
from notification.notification import notify


class Login(object):
    def __init__(self, parent):
        self.builders = Builders()
        self.conf = Configs()
        self.parent = parent
        self.api = YandexAPI()
        self.validation_error = wx.StaticText()
        self.sizer = wx.BoxSizer()
        self.dialog = wx.Dialog()
        self.main_pnl = self.parent.panel
        self.url = "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
        self.wv = None
        self.backend = self.getBackend()
        self.panel = None

    def create_login_popup(self):
        self.dialog = dialog = wx.Dialog(parent=self.parent, id=wx.ID_ANY,
                                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                                         name="login_popup_test")
        self.wv = webview.WebView.New(self.dialog, backend=self.backend)
        self.dialog.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.wv, 1, wx.EXPAND)
        dialog.SetSizer(sizer)
        self.wv.LoadURL(self.url)
        dialog.Center()
        dialog.Show()

    def on_logout_menu(self, event):
        self.api.logout()
        self.create_login_popup()
        self.parent.make_menu()

    def OnWebViewNavigating(self, event):
        if "access_token" in event.GetURL():
            event.Veto()
            qs = parse_qs(urlparse(event.GetURL().replace('#access_token', '?access_token')).query)
            self.conf.set_attr('token', qs['access_token'][0])
            self.conf.set_attr('token_exp', qs['expires_in'][0])
            self.api.login()
            notify(subtitle="Hello " + self.api.get_display_name())
            self.dialog.Destroy()

    def getBackend(self):
        backends = [
            (webview.WebViewBackendEdge, 'WebViewBackendEdge'),
            (webview.WebViewBackendIE, 'WebViewBackendIE'),
            (webview.WebViewBackendWebKit, 'WebViewBackendWebKit'),
            (webview.WebViewBackendDefault, 'WebViewBackendDefault'),
        ]
        for identifier, name in backends:
            available = webview.WebView.IsBackendAvailable(identifier)
            if available:
                print("Using backend: '{}'\n".format(str(identifier, 'ascii')))
                return identifier
