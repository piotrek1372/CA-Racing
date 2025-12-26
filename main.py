import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import load_game_assets
from menu import Menu, Button
from player import Player
from localization import LanguageManager
from settings import SettingsMenu

class GameSession:
    def __init__(self, main_app, slot_id):
        self.app = main_app
        self.slot_id = slot_id
        
        self.screen = main_app.screen
        self.assets = main_app.assets
        self.data_manager = main_app.data_manager
        self.lang = main_app.lang
        
        self.game_db = self.data_manager.load_game_data()
        self.player_save_data = self.data_manager.load_player_state(slot_id)
        self.player = Player(self.player_save_data, self.game_db)
        
        # Apply player's stored settings immediately upon load
        self.app.apply_graphics_settings(self.player.settings)
        
        self.font_header = pg.font.SysFont('Consolas', 32, bold=True)
        self.font_ui = pg.font.SysFont('Consolas', 24)
        
        self.state = 'HUB'
        self.buttons = []
        self.init_hub_ui()
        
        # We also need an instance of settings here for in-game access
        self.settings_menu = SettingsMenu(self.app, self.return_to_hub)
        
        print(f"[GAME] Session started. Player: {self.player.name}")

    def init_hub_ui(self):
        """Initializes Hub buttons based on current screen size."""
        self.buttons = []
        # Recalculate center based on current resolution
        w, h = self.app.screen.get_size()
        center_x = w // 2
        start_y = 200
        gap_y = 70
        
        options = [
            (self.lang.get("hub_race"), lambda: self.change_state('RACE'), ACCENT_GREEN),
            (self.lang.get("hub_garage"), lambda: self.change_state('GARAGE'), None),
            (self.lang.get("hub_shop"), lambda: self.change_state('SHOP'), None),
            (self.lang.get("hub_settings"), lambda: self.change_state('SETTINGS'), None),
            (self.lang.get("hub_main_menu"), self.exit_to_main_menu, ACCENT_RED)
        ]
        
        for i, (text, action, color) in enumerate(options):
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(text, pos, action, custom_color=color))

    def change_state(self, new_state):
        self.state = new_state
        if new_state == 'SETTINGS':
            self.settings_menu.init_main_view()

    def return_to_hub(self):
        self.change_state('HUB')
        # Re-init Hub UI in case resolution changed in settings
        self.init_hub_ui()

    def exit_to_main_menu(self):
        print(f"[GAME] Auto-saving to Slot {self.slot_id}...")
        save_data = self.player.to_dict()
        self.data_manager.save_player_state(self.slot_id, save_data)
        self.app.close_game_session()

    def update(self, events):
        if self.state == 'HUB':
            for event in events:
                for btn in self.buttons:
                    btn.handle_event(event)
        
        elif self.state == 'SETTINGS':
            for event in events:
                self.settings_menu.update(event)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.state == 'SETTINGS':
                        self.return_to_hub()
                    elif self.state != 'HUB':
                        self.change_state('HUB')

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_player_info()
        
        if self.state == 'HUB':
            self.draw_hub()
        elif self.state == 'SETTINGS':
            self.settings_menu.draw(self.screen)
        else:
            self.draw_placeholder(f"{self.state} - {self.lang.get('msg_esc')}")

    def draw_player_info(self):
        w, h = self.screen.get_size()
        pg.draw.rect(self.screen, PANEL_BG, (0, 0, w, 60))
        pg.draw.line(self.screen, ACCENT_BLUE, (0, 60), (w, 60), 2)
        
        label = self.lang.get("info_driver")
        name_surf = self.font_ui.render(f"{label}: {self.player.name}", True, TEXT_MAIN)
        self.screen.blit(name_surf, (20, 18))
        
        money_label = self.lang.get("info_money")
        money_text = f"{money_label}: ${self.player.money}"
        money_surf = self.font_ui.render(money_text, True, ACCENT_GOLD)
        money_rect = money_surf.get_rect(topright=(w - 20, 18))
        self.screen.blit(money_surf, money_rect)

    def draw_hub(self):
        for btn in self.buttons:
            btn.draw(self.screen)
            
        # Quality Check: Draw cars/details only if Quality is NOT LOW
        quality = self.player.settings.get("quality", "HIGH")
        
        if quality != "LOW":
            if 'cars' in self.assets and self.assets['cars']:
                car_sprite = self.assets['cars'].subsurface((0, 0, 64, 64))
                car_scaled = pg.transform.scale(car_sprite, (128, 128))
                self.screen.blit(car_scaled, (100, 250))
            
            # (Example) If High, we could draw particle effects or shadows here
            if quality == "HIGH":
                # Placeholder for high quality extra rendering
                pass

    def draw_placeholder(self, text):
        w, h = self.screen.get_size()
        text_surf = self.font_header.render(text, True, TEXT_DIM)
        rect = text_surf.get_rect(center=(w//2, h//2))
        self.screen.blit(text_surf, rect)

class Main:
    def __init__(self):
        pg.init()
        
        # Default global settings (before any save is loaded)
        self.global_settings = {
            "resolution_idx": 0,
            "fullscreen": False,
            "max_fps": 60,
            "quality": "HIGH"
        }
        
        # Initial Window Setup
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'MENU'
        self.lang = LanguageManager() 
        
        try:
            self.assets = load_game_assets()
        except Exception as e:
            print(f"[MAIN] Warning: {e}")
            self.assets = {}
            
        self.data_manager = Data()
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self, self.return_to_menu)
        self.game_session = None

    def apply_graphics_settings(self, settings_dict=None):
        """
        Applies graphics settings (Resolution, Fullscreen, FPS) to the Pygame Display.
        """
        # Determine which settings to use (Passed ones, Session ones, or Global)
        if settings_dict:
            target = settings_dict
        elif self.game_session:
            target = self.game_session.player.settings
        else:
            target = self.global_settings
            
        # 1. Resolution & Fullscreen
        res_idx = target.get("resolution_idx", 0)
        # Safety check
        if res_idx >= len(RESOLUTIONS): res_idx = 0
        
        width, height = RESOLUTIONS[res_idx]
        flags = pg.DOUBLEBUF
        if target.get("fullscreen", False):
            flags |= pg.FULLSCREEN
        
        # Re-create the window
        # Note: This might be slow on some systems
        self.screen = pg.display.set_mode((width, height), flags)
        
        # 2. Update logic related to screen size?
        # Not strictly needed if all draw calls use self.screen.get_size()
        # But we should inform active menus to re-calculate button positions
        if self.state == 'MENU':
            self.menu.init_main_menu()
        elif self.state == 'SETTINGS_MENU':
            self.settings_menu.init_graphics_view()

    def open_settings_from_menu(self):
        self.state = 'SETTINGS_MENU'
        self.settings_menu.init_main_view()

    def return_to_menu(self):
        self.state = 'MENU'
        self.menu.init_main_menu()

    def start_game_session(self, slot_id):
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            if not self.data_manager.create_new_save(slot_id):
                return
        try:
            self.game_session = GameSession(self, slot_id)
            self.state = 'GAME'
        except Exception as e:
            print(f"[MAIN] Error: {e}")

    def close_game_session(self):
        self.game_session = None
        # Re-apply global settings or keep last? 
        # Usually better to revert to defaults or keep last applied.
        # Let's keep current window state to avoid flickering.
        self.state = 'MENU'
        self.menu.init_main_menu()

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
            
            # Determine max FPS based on current context
            fps_limit = FPS # Default from constants
            if self.game_session:
                fps_limit = self.game_session.player.settings.get("max_fps", 60)
            else:
                fps_limit = self.global_settings.get("max_fps", 60)

            if self.state == 'MENU':
                for event in events:
                    self.menu.update(event)
                self.menu.draw(self.screen)
            
            elif self.state == 'SETTINGS_MENU':
                for event in events:
                    self.settings_menu.update(event)
                self.settings_menu.draw(self.screen)
                
            elif self.state == 'GAME':
                if self.game_session:
                    self.game_session.update(events)
                    if self.game_session: # Check existance again
                        self.game_session.draw()

            pg.display.flip()
            self.clock.tick(fps_limit)
        
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    app = Main()
    app.run()