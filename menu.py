import pygame as pg
from constants import *

class Button:
    def __init__(self, text, center_pos, action, custom_color=None):
        self.text = text
        self.action = action
        self.font_size = 35
        self.font = pg.font.SysFont('Consolas', self.font_size, bold=True)
        self.color_idle = custom_color if custom_color else BUTTON_COLOR
        self.color_hover = BUTTON_HOVER_COLOR
        self.text_color = TEXT_MAIN
        self.border_color = TEXT_DIM
        
        # Size & Rect
        text_width, text_height = self.font.size(self.text)
        padding_x, padding_y = 30, 15
        self.width = text_width + padding_x
        self.height = text_height + padding_y
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = center_pos
        
        # Shadow
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.x += 3
        self.shadow_rect.y += 3
        
        # Text Surface
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.color_hover if is_hovered else self.color_idle
        
        pg.draw.rect(screen, (15, 15, 20), self.shadow_rect, border_radius=8)
        pg.draw.rect(screen, current_color, self.rect, border_radius=8)
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class InputBox:
    """Simple text input for changing names."""
    def __init__(self, center_pos, initial_text=''):
        self.font = pg.font.SysFont('Consolas', 35, bold=True)
        self.rect = pg.Rect(0, 0, 300, 50)
        self.rect.center = center_pos
        self.color = TEXT_DIM
        self.text = initial_text
        self.txt_surface = self.font.render(self.text, True, TEXT_MAIN)
        self.active = True

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    pass # Handled by Save button externally
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limit length
                    if len(self.text) < 12:
                        self.text += event.unicode
                # Re-render
                self.txt_surface = self.font.render(self.text, True, TEXT_MAIN)

    def draw(self, screen):
        # Draw box
        pg.draw.rect(screen, (0,0,0), self.rect)
        pg.draw.rect(screen, self.color, self.rect, 2)
        # Draw text centered
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

class Menu:
    def __init__(self, main_app):
        self.app = main_app
        self.state = "main"
        self.buttons = []
        self.title_font = pg.font.SysFont('Consolas', 60, bold=True)
        self.init_main_menu()

    def _get_center_x(self):
        return self.app.screen.get_width() // 2

    def init_main_menu(self):
        self.state = "main"
        self.buttons = []
        center_x = self._get_center_x()
        start_y = 250
        gap_y = 70

        options = [
            (self.app.lang.get("menu_play"), self.go_to_saves, None),
            (self.app.lang.get("menu_options"), self.app.open_global_settings, None),
            (self.app.lang.get("menu_exit"), self.app.quit_game, ACCENT_RED)
        ]

        for i, (text, action, color) in enumerate(options):
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(text, pos, action, custom_color=color))

    def init_save_menu(self):
        self.state = "saves"
        self.buttons = []
        center_x = self._get_center_x()
        start_y = 200
        gap_y = 80
        
        slots = self.app.data_manager.check_save_slots()
        prefix = self.app.lang.get("slot_prefix")
        txt_load = self.app.lang.get("slot_load")
        txt_new = self.app.lang.get("slot_new")
        
        for i in range(1, 4):
            occupied = slots[i]
            btn_text = f"{prefix} {i} [{txt_load}]" if occupied else f"{prefix} {i} [{txt_new}]"
            color = ACCENT_BLUE if occupied else ACCENT_GREEN
            
            action = lambda slot=i: self.app.start_game_session(slot)
            pos = (center_x, start_y + (i-1) * gap_y)
            self.buttons.append(Button(btn_text, pos, action, custom_color=color))
            
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + 3 * gap_y + 20), self.init_main_menu))

    def go_to_saves(self):
        self.init_save_menu()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        key = "title_slots" if self.state == "saves" else "title_main"
        title_surf = self.title_font.render(self.app.lang.get(key), True, TEXT_MAIN)
        title_rect = title_surf.get_rect(center=(self._get_center_x(), 100))
        screen.blit(title_surf, title_rect)
        
        for btn in self.buttons:
            btn.draw(screen)