import pygame as pg
import sys
from src.constants import *
from src.core.data_manager import DataManager
from src.core.locale import LanguageManager
from src.core.assets import load_game_assets
from src.ui.menu_main import MainMenu
from src.ui.menu_settings import GlobalSettingsMenu
from src.game.session import GameSession

class Main:
    def __init__(self):
        pg.init()
        self.data_manager = DataManager()
        self.global_settings = self.data_manager.load_global_settings()
        
        self.lang = LanguageManager(self.global_settings.get("language", "en"))
        
        self.screen = None
        self.apply_graphics(self.global_settings)
        
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        
        try:
            self.assets = load_game_assets()
        except:
            self.assets = {}
            
        self.state = 'MENU'
        self.menu = MainMenu(self)
        self.settings = GlobalSettingsMenu(self, self.return_to_menu)
        self.session = None

    def apply_graphics(self, s):
        idx = s.get("resolution_idx", 0)
        idx = idx if idx < len(RESOLUTIONS) else 0
        w, h = RESOLUTIONS[idx]
        flags = pg.DOUBLEBUF
        if s.get("fullscreen"): flags |= pg.FULLSCREEN
        self.screen = pg.display.set_mode((w, h), flags)

    def start_game_session(self, slot_id):
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            if not self.data_manager.create_new_save(slot_id): return
        self.session = GameSession(self, slot_id)
        self.state = 'GAME'

    def close_session(self):
        self.session = None
        self.state = 'MENU'
        self.menu.init_main_view()

    def open_global_settings(self):
        self.state = 'SETTINGS'
        self.settings.init_main_view()

    def return_to_menu(self):
        self.state = 'MENU'
        self.menu.init_main_view()

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT: self.running = False
            
            if self.state == 'MENU':
                self.menu.update(events[0]) if events else None
                for e in events: self.menu.update(e)
                self.menu.draw(self.screen)
            elif self.state == 'SETTINGS':
                for e in events: self.settings.update(e)
                self.settings.draw(self.screen)
            elif self.state == 'GAME' and self.session:
                self.session.update(events)
                if self.session: self.session.draw()

            pg.display.flip()
            self.clock.tick(self.global_settings.get("max_fps", 60))
        
        pg.quit()
        sys.exit()