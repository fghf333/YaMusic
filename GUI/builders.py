import os

import wx
import wx.lib.buttons as buttons

from configs.configs import Configs


class Builders(object):
    def __init__(self):
        self.conf = Configs()
        if 'RESOURCEPATH' in os.environ:
            self.bitmapDir = '{}/assets'.format(os.environ['RESOURCEPATH'])
        else:
            self.dirName = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.bitmapDir = os.path.join(self.dirName, 'assets')
        pass

    def button_builder(self, parent, label, name):
        button = wx.Button(parent, label=label, name=name)
        button.SetForegroundColour(self.conf.get_attr("TEXT_COLOR"))
        button.SetBackgroundColour(self.conf.get_attr("BACKGROUND_COLOR"))
        return button

    def input_builder(self, parent, name, size=(250, 20), value=""):
        input_field = wx.TextCtrl(parent, size=size, name=name, value=value)
        input_field.SetBackgroundColour(self.conf.get_attr("BACKGROUND_COLOR"))
        input_field.SetForegroundColour(self.conf.get_attr("TEXT_COLOR"))
        return input_field

    def static_text_builder(self, parent, label):
        text = wx.StaticText(parent, label=label)
        text.SetForegroundColour(self.conf.get_attr("TEXT_COLOR"))
        return text

    def build_bitmap_button(self, btn_dict):

        handler = btn_dict['handler']
        name = btn_dict['name']
        parent = btn_dict['parent']
        size_h = btn_dict['size_h']
        size_w = btn_dict['size_w']

        img = wx.Image(os.path.join(self.bitmapDir, btn_dict['bitmap']), wx.BITMAP_TYPE_PNG)
        img = img.Scale(size_w, size_h, wx.IMAGE_QUALITY_HIGH)
        img = wx.Bitmap(img)
        btn = buttons.GenBitmapButton(parent=parent, bitmap=img, name=name)
        btn.Bind(wx.EVT_BUTTON, handler)
        return btn
