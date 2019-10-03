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
            self.bitmapDir = '{}/assets'.format(os.environ['RESOURCEPATH'])
        else:
            self.dirName = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.bitmapDir = os.path.join(self.dirName, 'assets')
        pass

        self.playback_slider = None
        self.main_pnl = None
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

        # create a panel in the frame
        main_pnl = self.main_pnl = wx.Panel(self.parent)
        main_pnl.SetBackgroundColour(self.conf.get_attr("BACKGROUND_COLOR"))

        self.playback_slider = self.toggle_gauge_slider()

        # and put some text with a larger bold font on it
        label = "Hello " + self.api.get_display_name()
        self.parent.st = wx.StaticText(main_pnl, label=label, name="greetings")

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        work_sizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbar = self.build_audio_bar()

        main_sizer.Add(
            self.playback_slider,
            0,
            wx.ALL | wx.EXPAND,
            1
        )

        work_sizer.Add(
            self.parent.st,
            0,
            wx.ALIGN_LEFT | wx.TOP,
            20
        )

        main_sizer.Add(
            work_sizer
        )

        main_sizer.Add(
            toolbar,
            0,
            wx.TOP,
            self.parent.GetSize()[1] - 120
        )

        font = self.parent.st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.parent.st.SetFont(font)

        main_pnl.SetSizer(main_sizer)

        return main_pnl

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

        audio_bar_sizer.Add(
            self.prev_track,
            0
        )

        img = wx.Image(os.path.join(self.bitmapDir, "player_play.png"), wx.BITMAP_TYPE_ANY)
        img = img.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        img = wx.Bitmap(img)
        self.play_pause_btn = buttons.GenBitmapToggleButton(self.main_pnl, bitmap=img, name="play")
        self.play_pause_btn.Enable(False)

        img = wx.Bitmap(os.path.join(self.bitmapDir, "player_pause.png"))
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

        self.next_track.Disable()
        self.prev_track.Disable()

        return audio_bar_sizer

    def enable_play_button(self):
        self.play_pause_btn.Enable(True)
