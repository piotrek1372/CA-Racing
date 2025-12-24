import pygame as pg
from pygame import Vector2
import constants as con
pg.init()
pg.font.init()

class Button:
    def __init__(self, text, index, action):
        self.text = text
        self.font_size = 35
        self.topleft = con.screen.get_size()[0] / 2 + 175, index * 35 + 150
        self.rect = pg.Rect(self.topleft[0], self.topleft[1], 100, 35)
        self.action = action
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
    def draw(self, screen):
        self.font = pg.Font(None, self.font_size)
        self.font = self.font.render(self.text, 1, (230, 230, 200))
        screen.blit(self.font, (self.rect[0], self.rect[1]))

class Box:
    def __init__(self, bts_count):
        self.size = con.screen.get_size()[0] / 3, bts_count * 35 + 80
        self.pos = con.screen.get_size()[0] / 2 + 100, 125
        self.rect = pg.Surface(self.size, flags=pg.SRCALPHA).convert_alpha()
    def draw(self, screen):
        self.rect.fill((15, 5, 200))
        screen.blit(self.rect, self.pos, special_flags=pg.BLEND_MULT)