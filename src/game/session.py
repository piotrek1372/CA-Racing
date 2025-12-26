import pygame as pg
from src.constants import *
from src.game.player import Player
from src.ui.widgets import Button
from src.ui.menu_settings import PlayerSettingsMenu

class GameSession:
    def __init__(self, app, slot_id):
        self.app = app
        self.slot_id = slot_id
        self.game_db = app.data_manager.load_game_data()
        self.player_data = app.data_manager.load_player_state(slot_id)
        self.player = Player(self.player_data, self.game_db)
        
        self.state = 'HUB'
        self.buttons = []
        self.player_menu = PlayerSettingsMenu(app, self.player, self.return_to_hub)
        self.init_hub()
        print(f"[GAME] Started. Player: {self.player.name}")

    def init_hub(self):
        self.buttons = []
        cx = self.app.screen.get_width() // 2
        y, gap = 200, 70
        opts = [
            ("hub_race", lambda: self.set_state('RACE'), ACCENT_GREEN),
            ("hub_garage", lambda: self.set_state('GARAGE'), None),
            ("hub_shop", lambda: self.set_state('SHOP'), None),
            ("hub_settings", lambda: self.set_state('PLAYER_SETTINGS'), None),
            ("hub_main_menu", self.exit, ACCENT_RED)
        ]
        for i, (k, act, col) in enumerate(opts):
            self.buttons.append(Button(self.app.lang.get(k), (cx, y+i*gap), act, custom_color=col))

    def set_state(self, st):
        self.state = st
        if st == 'PLAYER_SETTINGS': self.player_menu.init_ui()

    def return_to_hub(self):
        self.set_state('HUB')

    def exit(self):
        self.app.data_manager.save_player_state(self.slot_id, self.player.to_dict())
        self.app.close_session()

    def update(self, events):
        if self.state == 'HUB':
            for e in events: 
                for b in self.buttons: b.handle_event(e)
        elif self.state == 'PLAYER_SETTINGS':
            for e in events: self.player_menu.update(e)
        
        for e in events:
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                if self.state == 'PLAYER_SETTINGS': self.return_to_hub()
                elif self.state != 'HUB': self.set_state('HUB')

    def draw(self):
        self.app.screen.fill(BG_COLOR)
        self.draw_info()
        if self.state == 'HUB':
            for b in self.buttons: b.draw(self.app.screen)
            # Draw car example
            if 'cars' in self.app.assets and self.app.assets['cars']:
                c = pg.transform.scale(self.app.assets['cars'].subsurface((0,0,64,64)), (128,128))
                self.app.screen.blit(c, (100, 250))
        elif self.state == 'PLAYER_SETTINGS':
            self.player_menu.draw(self.app.screen)
        else:
            self.draw_placeholder(self.state)

    def draw_info(self):
        w = self.app.screen.get_width()
        pg.draw.rect(self.app.screen, PANEL_BG, (0,0,w,60))
        pg.draw.line(self.app.screen, ACCENT_BLUE, (0,60), (w,60), 2)
        f = pg.font.SysFont('Consolas', 24)
        
        ns = f.render(f"{self.app.lang.get('info_driver')}: {self.player.name}", True, TEXT_MAIN)
        self.app.screen.blit(ns, (20, 18))
        ms = f.render(f"${self.player.money}", True, ACCENT_GOLD)
        self.app.screen.blit(ms, ms.get_rect(topright=(w-20, 18)))

    def draw_placeholder(self, txt):
        s = pg.font.SysFont('Consolas',32,bold=True).render(txt,True,TEXT_DIM)
        self.app.screen.blit(s, s.get_rect(center=(self.app.screen.get_width()//2, self.app.screen.get_height()//2)))