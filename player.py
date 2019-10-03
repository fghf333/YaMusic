import json
import os

import wx
import wx.media


class Player(object):
    def __init__(self, parent=None, slider=None):
        self.frame = parent
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        self.timer = wx.Timer(parent)
        self.timer.Start(100)
        self.media_player = wx.media.MediaCtrl(parent, style=wx.SIMPLE_BORDER)
        self.slider = slider
        self.parent = parent
        self.playlist = None
        self.tracks = []
        self.current_track = 0
        self.min = 1
        self.max = 1
        for el in self.frame.GetChildren():
            if el.GetName() == 'prev':
                self.prev = el
            if el.GetName() == 'next':
                self.next = el

        if 'RESOURCEPATH' in os.environ:
            self.cache = '{}/cache'.format(os.environ['RESOURCEPATH'])
        else:
            self.dirName = os.path.dirname(os.path.abspath(__file__))
            self.cache = os.path.join(self.dirName, 'cache')
        pass

    def load_playlist(self, playlist):
        self.playlist = playlist
        with open('{}/{}/index.json'.format(self.cache, self.playlist), 'r') as file:
            file_parsed = json.load(file)
        self.current_track = file_parsed['last_track_num']
        self.max = len(file_parsed['tracks'])
        self.set_song()

    def set_song(self):
        with open('{}/{}/index.json'.format(self.cache, self.playlist), 'r') as file:
            file_parsed = json.load(file)

        tracks = file_parsed['tracks']

        for track in tracks:
            if track['num'] == self.current_track:
                music_file = '{}/{}/{}.mp3'.format(self.cache, self.playlist, track['num'])

                if not self.media_player.Load(music_file):
                    wx.MessageBox("Unable to load %s: Unsupported format?" % music_file,
                                  "ERROR",
                                  wx.ICON_ERROR | wx.OK)
                else:
                    self.media_player.SetInitialSize()
                    self.slider.SetRange(0, self.media_player.Length())
                    self.parent.Bind(wx.EVT_TIMER, self.on_timer)
        if self.current_track <= self.min:
            self.prev.Disable()
        else:
            self.prev.Enable()

        if self.current_track >= self.max:
            self.next.Disable()
        else:
            self.next.Enable()

    def on_timer(self, event):
        offset = self.media_player.Tell()
        self.slider.SetValue(offset)
        if offset == self.media_player.Length():
            self.on_next(event)

    def on_pause(self, event):
        self.media_player.Pause()

    def on_play(self, event):
        if not event.GetIsDown():
            self.on_pause(event)
            return

        if not self.media_player.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.media_player.SetInitialSize()
            self.slider.SetRange(0, self.media_player.Length())

        event.Skip()

    def on_seek(self, event):
        offset = self.slider.GetValue()
        self.media_player.Seek(offset)

    def on_next(self, event):
        if self.current_track + 1 > self.max:
            event.Skip()
        else:
            self.current_track += 1
            self.set_song()
            self.media_player.Play()

    def on_prev(self, event):
        if self.current_track - 1 < self.min:
            event.Skip()
        else:
            self.current_track -= 1
            self.set_song()
            self.media_player.Play()
