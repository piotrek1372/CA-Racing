import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import load_game_assets
from menu import Menu, Button
from player import Player
from localization import LanguageManager
from settings import GlobalSettingsMenu, PlayerSettingsMenu

class GameSession:
    def __init__(self, main_app, slot_id):
        self.app = main_app
        self.slot_id = slot_id
        
        self.screen = main_app.screen
        self.assets = main_app.assets
        self.data_manager = main_app.data_manager
        self.lang = main_app.lang
        
        # Load data
        self.game_db = self.data_manager.load_game_data()
        self.player_save_data = self.data_manager.load_player_state(slot_id)
        self.player = Player(self.player_save_data, self.game_db)
        
        self.font_header = pg.font.SysFont('Consolas', 32, bold=True)
        self.font_ui = pg.font.SysFont('Consolas', 24)
        
        self.state = 'HUB'
        self.buttons = []
        self.init_hub_ui()
        
        # Setup Player Settings Menu (Rename only)
        self.player_settings_menu = PlayerSettingsMenu(self.app, self.player, self.return_to_hub)
        
        print(f"[GAME] Session started. Player: {self.player.name}")

    def init_hub_ui(self):
        self.buttons = []
        cx = self.screen.get_width() // 2
        y = 200
        gap = 70
        
        opts = [
            (self.lang.get("hub_race"), lambda: self.change_state('RACE'), ACCENT_GREEN),
            (self.lang.get("hub_garage"), lambda: self.change_state('GARAGE'), None),
            (self.lang.get("hub_shop"), lambda: self.change_state('SHOP'), None),
            (self.lang.get("hub_settings"), lambda: self.change_state('PLAYER_SETTINGS'), None),
            (self.lang.get("hub_main_menu"), self.exit_to_main_menu, ACCENT_RED)
        ]
        
        for i, (txt, act, col) in enumerate(opts):
            self.buttons.append(Button(txt, (cx, y + i*gap), act, custom_color=col))

    def change_state(self, new_state):
        self.state = new_state
        if new_state == 'PLAYER_SETTINGS':
            self.player_settings_menu.init_ui() # Refresh name in input box

    def return_to_hub(self):
        self.change_state('HUB')
        # Rename might have happened, update UI?
        # Ideally Hub UI doesn't display name on buttons, but HUD does.

    def exit_to_main_menu(self):
        print(f"[GAME] Auto-saving slot {self.slot_id}...")
        self.data_manager.save_player_state(self.slot_id, self.player.to_dict())
        self.app.close_game_session()

    def update(self, events):
        if self.state == 'HUB':
            for e in events:
                for b in self.buttons: b.handle_event(e)
        elif self.state == 'PLAYER_SETTINGS':
            for e in events:
                self.player_settings_menu.update(e)
        
        # ESC handling
        for e in events:
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                if self.state == 'PLAYER_SETTINGS':
                    self.return_to_hub()
                elif self.state != 'HUB':
                    self.change_state('HUB')

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_player_info()
        
        if self.state == 'HUB':
            self.draw_hub()
        elif self.state == 'PLAYER_SETTINGS':
            self.player_settings_menu.draw(self.screen)
        else:
            self.draw_placeholder(f"{self.state}")

    def draw_player_info(self):
        w = self.screen.get_width()
        pg.draw.rect(self.screen, PANEL_BG, (0,0,w,60))
        pg.draw.line(self.screen, ACCENT_BLUE, (0,60), (w,60), 2)
        
        lbl = self.lang.get("info_driver")
        name_s = self.font_ui.render(f"{lbl}: {self.player.name}", True, TEXT_MAIN)
        self.screen.blit(name_s, (20, 18))
        
        money_s = self.font_ui.render(f"${self.player.money}", True, ACCENT_GOLD)
        m_rect = money_s.get_rect(topright=(w-20, 18))
        self.screen.blit(money_s, m_rect)

    def draw_hub(self):
        for b in self.buttons: b.draw(self.screen)
        if 'cars' in self.assets and self.assets['cars']:
            # Example drawing
            car = pg.transform.scale(self.assets['cars'].subsurface((0,0,64,64)), (128,128))
            self.screen.blit(car, (100, 250))

    def draw_placeholder(self, txt):
        s = self.font_header.render(txt, True, TEXT_DIM)
        r = s.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(s, r)

class Main:
    def __init__(self):
        pg.init()
        self.data_manager = Data()
        
        # 1. Load Global Settings
        self.global_settings = self.data_manager.load_global_settings()
        
        # 2. Setup Language based on Global Settings
        self.lang = LanguageManager(self.global_settings.get("language", "en"))
        
        # 3. Apply Graphics
        self.screen = None # Created in apply_graphics_settings
        self.apply_graphics_settings(self.global_settings)
        
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'MENU'
        
        try:
            self.assets = load_game_assets()
        except:
            self.assets = {}
            
        self.menu = Menu(self)
        self.global_settings_menu = GlobalSettingsMenu(self, self.return_to_menu)
        self.game_session = None

    def apply_graphics_settings(self, settings):
        res_idx = settings.get("resolution_idx", 0)
        idx = res_idx if res_idx < len(RESOLUTIONS) else 0
        w, h = RESOLUTIONS[idx]
        flags = pg.DOUBLEBUF
        if settings.get("fullscreen"): flags |= pg.FULLSCREEN
        self.screen = pg.display.set_mode((w, h), flags)

    def open_global_settings(self):
        self.state = 'GLOBAL_SETTINGS'
        self.global_settings_menu.init_main_view()

    def return_to_menu(self):
        self.state = 'MENU'
        self.menu.init_main_menu()

    def start_game_session(self, slot_id):
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            if not self.data_manager.create_new_save(slot_id): return
        try:
            self.game_session = GameSession(self, slot_id)
            self.state = 'GAME'
        except Exception as e:
            print(f"[MAIN] Error: {e}")

    def close_game_session(self):
        self.game_session = None
        self.state = 'MENU'
        self.menu.init_main_menu()

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT: self.running = False
            
            fps = self.global_settings.get("max_fps", 60)
            
            if self.state == 'MENU':
                for e in events: self.menu.update(e)
                self.menu.draw(self.screen)
            
            elif self.state == 'GLOBAL_SETTINGS':
                for e in events: self.global_settings_menu.update(e)
                self.global_settings_menu.draw(self.screen)
                
            elif self.state == 'GAME':
                if self.game_session:
                    self.game_session.update(events)
                    if self.game_session: self.game_session.draw()

            pg.display.flip()
            self.clock.tick(fps)
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    app = Main()
    app.run()