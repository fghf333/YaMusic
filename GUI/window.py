import wx

import events.events as events
from GUI import builders, login, main_panel
from configs.configs import Configs
from music.API import YandexAPI
from notification.notification import notify
from player import Player


# import logging
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Window(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent"s __init__ is called
        super(Window, self).__init__(*args, **kw)

        self.conf = Configs()
        self.api = YandexAPI()
        self.builders = builders.Builders()
        self.panel = main_panel.MainPanel(self)
        self.login = login.Login(self)

        self.SetTitle(self.conf.get_attr("APP_TITLE"))
        self.main_pnl = self.panel.make_main_panel()
        self.input = wx.TextCtrl()
        self.gauge = self.panel.playback_slider
        self.player = Player(parent=self.main_pnl, slider=self.gauge)
        self.playlists_list = None
        self.account_menu = None
        self.playlist_selection = None
        self.playlists = None

        self.Bind(events.FIRST_TRACK_APPEAR, self.on_first_track)
        self.Bind(events.PLAYLIST_READY, self.on_playlist_ready)
        self.gauge.Bind(wx.EVT_SLIDER, self.player.on_seek)

        self.make_menu()
        self.Center()
        self.Show()

        if not self.api.is_logged_in() and wx.FindWindowByName("login_popup") is None:
            self.login.create_login_popup()

    def make_menu(self):

        # Make a file menu with Hello and Exit items
        self.account_menu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        if self.api.is_logged_in():
            logout = self.account_menu.Append(1, "&Logout\tCtrl-L", "Logout from account")
            self.Bind(wx.EVT_MENU, self.login.on_logout_menu, logout)

        player_menu = wx.Menu()

        self.playlists_list = wx.Menu(wx.ID_ANY)
        self.playlist_selection = player_menu.Append(wx.ID_ANY, "Playlists", self.playlists_list)
        if self.api.is_logged_in():
            self.playlists = self.api.get_play_lists_list()
            for playlist in self.playlists:
                self.Bind(
                    wx.EVT_MENU,
                    self.on_list_select,
                    self.playlists_list.Append(wx.ID_ANY, playlist['name'])
                )
            pass
        else:
            self.playlist_selection.Enable(False)
            pass

        # Now a help menu for the about item
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The "&" defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menu_bar = wx.MenuBar()
        menu_bar.Append(self.account_menu, "Account")
        menu_bar.Append(player_menu, "Player")
        menu_bar.Append(help_menu, "Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menu_bar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def on_first_track(self, event):
        playlist_type = event.playlist_type
        self.gauge.Enable()
        self.panel.enable_play_button()
        self.player.load_playlist(playlist_type)
        pass

    def on_playlist_ready(self, event):
        playlist_name = event.playlist_name
        playlist_type = event.playlist_type
        self.player.load_playlist(playlist_type)
        notify(playlist_name, "Playlist is ready", "")
        pass

    def on_prev(self, event):
        self.player.on_prev(event)
        pass

    def on_next(self, event):
        self.player.on_next(event)
        pass

    def on_play(self, event):
        if not event.GetIsDown():
            self.on_pause(event)
            return
        self.player.on_play(event)
        pass

    def on_pause(self, event):
        self.player.on_pause(event)
        pass

    def on_list_select(self, event):
        playlist_label = event.GetEventObject().GetLabelText(event.GetId())
        playlist_type = None
        for playlist in self.playlists:
            if playlist['name'] == playlist_label:
                playlist_type = playlist['type']
        self.api.preparation(playlist_type, self)

    def on_exit(self, event):
        self.Close(True)

    def on_about(self, event):
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK | wx.ICON_ASTERISK)
