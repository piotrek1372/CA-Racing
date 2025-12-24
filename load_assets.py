import pygame as pg
import os

pg.init()

class Assets:
    def __init__(self):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.assets_dir = os.path.join(self.main_dir, 'assets')
    def load_image(self, image_group, name, colorkey=-1, scale=1):
        fullname = os.path.join(self.assets_dir, 'images', image_group, name)
        image = pg.image.load(fullname)
        image.convert_alpha()

        image = pg.transform.scale(image, scale)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pg.RLEACCEL)
        return image, image.get_rect()