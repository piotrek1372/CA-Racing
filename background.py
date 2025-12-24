import pygame as pg
import load_assets

pg.init()
assets = load_assets.Assets()

class Background(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = assets.load_image('maps', 'map_0.png', scale=(screen_width, screen_height))
        self.rect.topleft = 0, 0
