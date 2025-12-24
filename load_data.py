import pygame as pg
import os, json

pg.init()

class Data:
    def __init__(self):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, 'data')
    def load_saves_template(self, file_name):
        fullname = os.path.join(self.data_dir, 'saves', file_name)
        try:
            with open(fullname, mode='r', encoding='utf-8') as f:
                data = json.loads(f)
        except Exception as e:
            print(f"{e}")
        return data