import pygame as pg
from src.constants import *

class Button:
    def __init__(self, text, center_pos, action, app=None, custom_color=None):
        """
        :param app: Reference to main App for Audio access (optional).
        """
        self.text = text
        self.action = action
        self.app = app  # Needed for sound
        self.font = pg.font.SysFont('Consolas', 35, bold=True)
        self.color_idle = custom_color if custom_color else BUTTON_COLOR
        self.color_hover = BUTTON_HOVER_COLOR
        self.text_color = TEXT_MAIN
        self.border_color = TEXT_DIM
        
        text_width, text_height = self.font.size(self.text)
        self.rect = pg.Rect(0, 0, text_width + 30, text_height + 15)
        self.rect.center = center_pos
        
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.x += 3
        self.shadow_rect.y += 3
        
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.is_hovered = False

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        hover_now = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound only on state change
        if hover_now and not self.is_hovered:
            if self.app and hasattr(self.app, 'audio'):
                self.app.audio.play_sfx('ui_hover')
        
        self.is_hovered = hover_now
        col = self.color_hover if self.is_hovered else self.color_idle
        
        pg.draw.rect(screen, (15, 15, 20), self.shadow_rect, border_radius=8)
        pg.draw.rect(screen, col, self.rect, border_radius=8)
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # Play Click Sound
                if self.app and hasattr(self.app, 'audio'):
                    if self.action: # Validation sound vs Success sound
                        self.app.audio.play_sfx('ui_click')
                    else:
                        self.app.audio.play_sfx('ui_error')
                
                if self.action:
                    self.action()

class InputBox:
    def __init__(self, center_pos, initial_text='', app=None):
        self.app = app
        self.font = pg.font.SysFont('Consolas', 35, bold=True)
        self.rect = pg.Rect(0, 0, 300, 50)
        self.rect.center = center_pos
        self.color = TEXT_DIM
        self.text = initial_text
        self.txt_surface = self.font.render(self.text, True, TEXT_MAIN)
        self.active = True

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                if self.app: self.app.audio.play_sfx('ui_select')
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.app: self.app.audio.play_sfx('ui_hover') # Typing sound effect
            else:
                if len(self.text) < 12:
                    self.text += event.unicode
                    if self.app: self.app.audio.play_sfx('ui_hover')
            self.txt_surface = self.font.render(self.text, True, TEXT_MAIN)

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,0), self.rect)
        pg.draw.rect(screen, self.color, self.rect, 2)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)