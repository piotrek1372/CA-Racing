import pygame as pg
from constants import *
pg.init()
pg.font.init()

class Button:
    def __init__(self, text, index, action):
        self.text = text
        self.font_size = 35
        self.font = pg.font.SysFont('Consolas', self.font_size, bold=True)
        text_width, text_height = self.font.size(text)
        self.topleft = SCREEN.get_size()[0] / 2 + 175, index * 60 + 150
        self.rect = pg.Rect(self.topleft[0], self.topleft[1], text_width + 20, text_height + 10)
        self.color_idle = BUTTON_COLOR
        self.color_hover = BUTTON_HOVER_COLOR
        self.text_color = TEXT_MAIN
        self.border_color = TEXT_DIM
        self.action = action
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.color_hover if is_hovered else self.color_idle

        pg.draw.rect(screen, (15, 15, 20), (self.rect.x + 3, self.rect.y + 3, self.rect.width, self.rect.height), border_radius=5)

        pg.draw.rect(screen, current_color, self.rect, border_radius=5)
        
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class Box:
    def __init__(self, bts_count):
        self.size = SCREEN.get_size()[0] / 3, bts_count * 35 + 80
        self.pos = SCREEN.get_size()[0] / 2 + 100, 125
        self.rect = pg.Surface(self.size, flags=pg.SRCALPHA).convert_alpha()
    def draw(self, screen):
        self.rect.fill((15, 5, 200))
        screen.blit(self.rect, self.pos, special_flags=pg.BLEND_MULT)