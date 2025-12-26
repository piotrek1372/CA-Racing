import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import load_game_assets
from menu import Menu, Button
from player import Player
from localization import LanguageManager

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
        
        self.font_header = pg.font.SysFont('Consolas', 32, bold=True)
        self.font_ui = pg.font.SysFont('Consolas', 24)
        
        self.state = 'HUB'
        self.buttons = []
        self.init_hub_ui()
        
        print(f"[GAME] Session started. Player: {self.player.name}")

    def init_hub_ui(self):
        self.buttons = []
        center_x = SCREEN_WIDTH // 2
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

    def exit_to_main_menu(self):
        self.app.close_game_session()

    def update(self, events):
        if self.state == 'HUB':
            for event in events:
                for btn in self.buttons:
                    btn.handle_event(event)
        
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.state != 'HUB':
                        self.change_state('HUB')

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_player_info()
        
        if self.state == 'HUB':
            self.draw_hub()
        else:
            self.draw_placeholder(f"{self.state} - {self.lang.get('msg_esc')}")

    def draw_player_info(self):
        pg.draw.rect(self.screen, PANEL_BG, (0, 0, SCREEN_WIDTH, 60))
        pg.draw.line(self.screen, ACCENT_BLUE, (0, 60), (SCREEN_WIDTH, 60), 2)
        
        label = self.lang.get("info_driver")
        name_surf = self.font_ui.render(f"{label}: {self.player.name}", True, TEXT_MAIN)
        self.screen.blit(name_surf, (20, 18))
        
        money_label = self.lang.get("info_money")
        money_text = f"{money_label}: ${self.player.money}"
        money_surf = self.font_ui.render(money_text, True, ACCENT_GOLD)
        money_rect = money_surf.get_rect(topright=(SCREEN_WIDTH - 20, 18))
        self.screen.blit(money_surf, money_rect)

    def draw_hub(self):
        for btn in self.buttons:
            btn.draw(self.screen)
        if 'cars' in self.assets and self.assets['cars']:
            # Drawing a car (example)
            car_sprite = self.assets['cars'].subsurface((0, 0, 64, 64))
            car_scaled = pg.transform.scale(car_sprite, (128, 128))
            self.screen.blit(car_scaled, (100, 250))

    def draw_placeholder(self, text):
        text_surf = self.font_header.render(text, True, TEXT_DIM)
        rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text_surf, rect)

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'MENU'
        
        # 1. Initialize Language (no argument = auto-detection)
        self.lang = LanguageManager() 
        
        try:
            self.assets = load_game_assets()
        except Exception as e:
            print(f"[MAIN] Warning: {e}")
            self.assets = {}
            
        self.data_manager = Data()
        self.menu = Menu(self)
        self.game_session = None

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
            
            if self.state == 'MENU':
                for event in events:
                    self.menu.update(event)
                self.menu.draw(self.screen)
            elif self.state == 'GAME':
                if self.game_session:
                    self.game_session.update(events)
                    self.game_session.draw()

            pg.display.flip()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    app = Main()
    app.run()