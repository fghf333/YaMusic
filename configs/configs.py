import json
import os
import shutil


class Configs(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Configs, cls)
            cls._instance = orig.__new__(cls, **kw)
        return cls._instance

    def __init__(self):

        if 'RESOURCEPATH' in os.environ:
            self.conf_file_path = '{}/configs'.format(os.environ['RESOURCEPATH'])
        else:
            self.dirName = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.conf_file_path = os.path.join(self.dirName, 'configs')
        pass
        conf_file_path = '{}/configs.json'.format(self.conf_file_path)

        if not os.path.isfile(conf_file_path):
            shutil.copyfile('{}/configs.json.dist'.format(self.conf_file_path), conf_file_path)

        conf_file_read = open(conf_file_path, "r+")
        self.confs = json.load(conf_file_read)
        conf_file_read.close()

    def get_attr(self, attr_name):
        if attr_name in self.confs:
            return self.confs[attr_name]
        else:
            return False

    def set_attr(self, attr_name, attr_value):
        self.confs[attr_name] = attr_value
        self.save_confs()
        return True

    def remove_attr(self, attr_name):
        self.confs.pop(attr_name, None)
        self.save_confs()
        return True

    def save_confs(self):
        conf_file_write = open('{}/configs.json'.format(self.conf_file_path), "w")
        json.dump(self.confs, conf_file_write)
        return True
