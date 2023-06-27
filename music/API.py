import json
import os
import threading
from datetime import date, datetime

import wx
from yandex_music.client import Client

import events.events as events
from configs.configs import Configs


class YandexAPI(object):

    def __init__(self):
        self.conf = Configs()
        self.client = self.login()
        self.win = None
        self.list_type = None
        self.playlists_list = None
        self.updating_thread = None

        if 'RESOURCEPATH' in os.environ:
            self.cache = '{}/cache'.format(os.environ['RESOURCEPATH'])
        else:
            self.dirName = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.cache = os.path.join(self.dirName, 'cache')
        pass

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(YandexAPI, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def login(self, login=None, password=None):
        if self.conf.get_attr("token") is not False:
            client = Client(self.conf.get_attr("token")).init()
        elif login is not None and password is not None:
            client = captcha_key = captcha_image_url = captcha_answer = None
            while not client:
                try:
                    client = Client.from_credentials(login, password, captcha_answer, captcha_key)
                except Exception as e:
                    if e.captcha.x_captcha_url:
                        captcha_image_url = e.captcha.x_captcha_url
                        captcha_key = e.captcha.x_captcha_key
                    else:
                        print('Вы отправили ответ не посмотрев на картинку.')

                    captcha_answer = input(f'{captcha_image_url}\nВведите код с картинки: ')

            token = client.token
            self.conf.set_attr("token", token)
            return client
        else:
            client = Client()
        self.client = client
        return client

    def is_logged_in(self):
        if self.client.me.account.display_name is None:
            return False
        else:
            return True

    def logout(self):
        self.conf.remove_attr("token")
        self.client = Client()
        pass

    def get_display_name(self):
        return str(self.login().me.account.display_name)

    def get_play_lists_list(self):
        entities = self.client.landing(blocks="personalplaylists").blocks[0].entities
        lists = []
        for playlist in entities:
            lists.append({
                "name": playlist.data.data.title,
                "type": playlist.data.type
            })
        self.playlists_list = lists
        return lists

    def preparation(self, list_type, win):
        self.updating_thread = threading.Thread(target=self.update)
        self.list_type = list_type
        self.win = win
        index = {
            "date": date.today().__str__(),
            "last_track_num": 1,
            "tracks": []
        }

        if not os.path.exists('{}/{}/'.format(self.cache, list_type)):
            os.mkdir('cache/{}'.format(list_type))

        if not os.path.exists('{}/{}/index.json'.format(self.cache, list_type)):
            with open('{}/{}/index.json'.format(self.cache, list_type), 'w+') as file:
                json.dump(index, file, indent=4)
            self.updating_thread.start()
        else:
            if self.is_need_update():
                with open('{}/{}/index.json'.format(self.cache, list_type), 'w+') as file:
                    json.dump(index, file, indent=4)
                self.updating_thread.start()
            else:
                wx.PostEvent(self.win, events.FirstTrackAppear(playlist_type=list_type))
                playlist_title = ""
                for playlist in self.playlists_list:
                    if playlist['type'] == list_type:
                        playlist_title = playlist['name']
                wx.PostEvent(self.win, events.PlaylistReady(playlist_name=playlist_title, playlist_type=list_type))
                return True

    def is_need_update(self):
        list_type = self.list_type
        with open('{}/{}/index.json'.format(self.cache, list_type), 'r') as file:
            index_date = datetime.strptime(json.load(file)['date'], '%Y-%m-%d').date()
            if index_date == date.today():
                return False
            else:
                return True

    def update(self):
        print("Starting update")
        list_type = self.list_type

        blocks = self.client.landing(blocks="personalplaylists").blocks[0].entities

        playlist = ""

        print("processing blocks")

        for block in blocks:
            if block.data.type == list_type:
                playlist = block.data.data

        tracks = self.client.users_playlists(playlist.kind, playlist.owner.uid).tracks
        index_file = json.load(open('{}/{}/index.json'.format(self.cache, list_type), 'r'))
        index = 1

        print("processing tracks")

        for track in tracks:

            if index == 2:
                wx.PostEvent(self.win, events.FirstTrackAppear(playlist_name=playlist.title, playlist_type=list_type))

            full_track_info = track.track
            index_file['tracks'].append({
                "id": full_track_info.id,
                "title": full_track_info.title,
                "artist": full_track_info.artists[0]['name'],
                "duration": full_track_info.duration_ms,
                "num": index
            })

            with open('{}/{}/index.json'.format(self.cache, list_type), 'w+') as file:
                json.dump(index_file, file)

            track.track.download_cover('{}/{}/{}.png'.format(self.cache, list_type, index))
            track.track.download('{}/{}/{}.mp3'.format(self.cache, list_type, index), codec="mp3", bitrate_in_kbps=320)

            if index == 3:
                break

            index = index + 1
        print("finishing updating")
        wx.PostEvent(self.win, events.PlaylistReady(playlist_name=playlist.title, playlist_type=list_type))
        return True
