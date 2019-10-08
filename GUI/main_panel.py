import os

import wx
import wx.lib.buttons as buttons

from GUI.builders import Builders
from configs.configs import Configs
from music.API import YandexAPI


class MainPanel(object):
    def __init__(self, parent):

        self.conf = Configs()
        self.parent = parent
        self.api = YandexAPI()
        self.builders = Builders()

        if 'RESOURCEPATH' in os.environ:
            self.asset_dir = '{}/assets'.format(os.environ['RESOURCEPATH'])
        else:
            self.dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.asset_dir = os.path.join(self.dir_name, 'assets')
        pass

        self.main_pnl = wx.Panel(parent)
        self.song_band = None
        self.song_name = None
        self.playback_slider = None
        self.play_pause_btn = None
        self.next_track = None
        self.prev_track = None

    def toggle_gauge_slider(self, slider_type='slider'):
        if slider_type == 'gauge':
            control = wx.Gauge(
                self.main_pnl,
                range=20,
                size=(self.parent.GetSize()[0], 5),
                style=wx.GA_HORIZONTAL | wx.GA_SMOOTH
            ).Pulse()
        else:
            control = wx.Slider(
                self.main_pnl,
                size=(self.parent.GetSize()[0], 5),
                minValue=0,
                maxValue=20
            )
            control.Disable()

        return control

    def make_main_panel(self):

        self.main_pnl.SetBackgroundColour(self.conf.get_attr("BACKGROUND_COLOR"))

        self.playback_slider = self.toggle_gauge_slider()

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        toolbar = self.build_audio_bar()

        main_sizer.Add(
            self.playback_slider,
            0,
            wx.ALL | wx.EXPAND,
            0
        )

        main_sizer.AddStretchSpacer(1)

        main_sizer.Add(
            self.playlist_list(),
            0
        )

        main_sizer.AddStretchSpacer(1)

        main_sizer.Add(
            toolbar,
            0
        )

        self.main_pnl.SetSizer(main_sizer)

        return self.main_pnl

    def build_audio_bar(self):
        """
        Builds the audio bar controls
        """
        audio_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.prev_track = self.builders.build_bitmap_button({
            'bitmap': 'player_prev.png',
            'handler': self.parent.on_prev,
            'name': 'prev',
            'parent': self.main_pnl,
            'size_h': 30,
            'size_w': 30
        })

        self.song_band = self.builders.static_text_builder(parent=self.main_pnl, label="")
        self.song_name = self.builders.static_text_builder(parent=self.main_pnl, label="")

        song_sizer = wx.BoxSizer(wx.VERTICAL)

        song_sizer.Add(
            self.song_band,
            0
        )

        song_sizer.Add(
            self.song_name,
            0
        )

        audio_bar_sizer.Add(
            self.prev_track,
            0
        )

        img = wx.Image(os.path.join(self.asset_dir, "player_play.png"), wx.BITMAP_TYPE_ANY)
        img = img.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        img = wx.Bitmap(img)
        self.play_pause_btn = buttons.GenBitmapToggleButton(self.main_pnl, bitmap=img, name="play")
        self.play_pause_btn.Enable(False)

        img = wx.Image(os.path.join(self.asset_dir, "player_pause.png"), wx.BITMAP_TYPE_ANY)
        img = img.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        img = wx.Bitmap(img)
        self.play_pause_btn.SetBitmapSelected(img)
        self.play_pause_btn.SetInitialSize()

        self.play_pause_btn.Bind(wx.EVT_BUTTON, self.parent.on_play)
        audio_bar_sizer.Add(
            self.play_pause_btn,
            0
        )

        self.next_track = self.builders.build_bitmap_button({
            'bitmap': 'player_next.png',
            'handler': self.parent.on_next,
            'name': 'next',
            'parent': self.main_pnl,
            'size_h': 30,
            'size_w': 30
        })

        audio_bar_sizer.Add(
            self.next_track,
            0
        )

        audio_bar_sizer.AddSpacer(5)

        audio_bar_sizer.Add(
            song_sizer,
            0
        )

        self.next_track.Disable()
        self.prev_track.Disable()

        return audio_bar_sizer

    def enable_play_button(self):
        self.play_pause_btn.Enable(True)

    def playlist_list(self):
        playlists_sizer = wx.BoxSizer(wx.HORIZONTAL)
        playlists_sizer.AddSpacer(5)
        playlists = [
            {
                "cover": "playlistOfTheDay",
                "parent": self.main_pnl
            },
            {
                "cover": "neverHeard",
                "parent": self.main_pnl
            },
            {
                "cover": "missedLikes",
                "parent": self.main_pnl
            },
            {
                "cover": "recentTracks",
                "parent": self.main_pnl
            }
        ]
        for playlist in playlists:
            item = self.builders.build_playlist_cover(playlist)
            playlists_sizer.Add(
                item,
                0
            )
            playlists_sizer.AddSpacer(5)
            item.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
            item.Bind(wx.EVT_LEAVE_WINDOW, self.on_unhover)
            item.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        return playlists_sizer

    def on_click(self, event):
        playlist_type = event.EventObject.GetName()
        self.api.preparation(playlist_type, self.parent)

    def on_unhover(self, event):
        event.EventObject.Stop()

    def on_hover(self, event):
        event.EventObject.Play()
