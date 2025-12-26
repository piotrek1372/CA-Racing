import pygame as pg
from src.constants import *
from src.ui.widgets import Button

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.state = "main"
        self.buttons = []
        self.title_font = pg.font.SysFont('Consolas', 60, bold=True)
        self.init_main_view()

    def _get_center_x(self):
        return self.app.screen.get_width() // 2

    def init_main_view(self):
        self.state = "main"
        self.buttons = []
        cx = self._get_center_x()
        start_y = 250
        gap = 70

        opts = [
            (self.app.lang.get("menu_play"), self.go_to_saves, None),
            (self.app.lang.get("menu_options"), self.app.open_global_settings, None),
            (self.app.lang.get("menu_exit"), self.app.quit_game, ACCENT_RED)
        ]

        for i, (txt, act, col) in enumerate(opts):
            self.buttons.append(Button(txt, (cx, start_y + i*gap), act, custom_color=col))

    def init_save_view(self):
        self.state = "saves"
        self.buttons = []
        cx = self._get_center_x()
        start_y = 200
        gap = 80
        
        slots = self.app.data_manager.check_save_slots()
        prefix = self.app.lang.get("slot_prefix")
        txt_load = self.app.lang.get("slot_load")
        txt_new = self.app.lang.get("slot_new")
        
        for i in range(1, 4):
            occupied = slots[i]
            btn_txt = f"{prefix} {i} [{txt_load}]" if occupied else f"{prefix} {i} [{txt_new}]"
            col = ACCENT_BLUE if occupied else ACCENT_GREEN
            
            action = lambda slot=i: self.app.start_game_session(slot)
            self.buttons.append(Button(btn_txt, (cx, start_y + (i-1)*gap), action, custom_color=col))
            
        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, start_y + 3*gap + 20), self.init_main_view))

    def go_to_saves(self):
        self.init_save_view()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        key = "title_slots" if self.state == "saves" else "title_main"
        title = self.app.lang.get(key)
        
        t_surf = self.title_font.render(title, True, TEXT_MAIN)
        t_rect = t_surf.get_rect(center=(self._get_center_x(), 100))
        screen.blit(t_surf, t_rect)
        
        for btn in self.buttons:
            btn.draw(screen)