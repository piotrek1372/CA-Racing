import pygame as pg
from src.constants import *
from src.game.player import Player
from src.ui.widgets import Button
from src.ui.menu_settings import PlayerSettingsMenu
from src.ui.menu_garage import GarageMenu
from src.core.assets import get_car_sprite

class GameSession:
    """
    Manages the active game session (Hub, Race, etc).
    """
    def __init__(self, app, slot_id):
        self.app = app
        self.slot_id = slot_id
        
        # Load Data
        self.game_db = app.data_manager.load_game_data()
        self.player_data = app.data_manager.load_player_state(slot_id)
        self.player = Player(self.player_data, self.game_db)
        
        self.state = 'HUB'
        self.buttons = []
        
        # Sub-menus
        self.player_menu = PlayerSettingsMenu(app, self.player, self.return_to_hub)
        self.garage_menu = GarageMenu(app, self.player, self.return_to_hub)
        
        self.init_hub()
        print(f"[GAME] Started. Player: {self.player.name}")

    def init_hub(self):
        """Initializes buttons for the main hub view."""
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
            self.buttons.append(Button(self.app.lang.get(k), (cx, y+i*gap), act, app=self.app, custom_color=col))

    def set_state(self, st):
        """Switches sub-state within the session."""
        self.state = st
        if st == 'PLAYER_SETTINGS': 
            self.player_menu.init_ui()
        elif st == 'GARAGE':
            self.garage_menu.init_ui() # Re-calculate grid in case inventory changed

    def return_to_hub(self):
        self.set_state('HUB')

    def exit(self):
        """Saves and exits to main menu."""
        self.app.data_manager.save_player_state(self.slot_id, self.player.to_dict())
        self.app.close_session()

    def update(self, events):
        """Central update delegation."""
        if self.state == 'HUB':
            for e in events: 
                for b in self.buttons: b.handle_event(e)
        elif self.state == 'PLAYER_SETTINGS':
            for e in events: self.player_menu.update(e)
        elif self.state == 'GARAGE':
            for e in events: self.garage_menu.update(e)
        
        # Global ESC to back/exit
        for e in events:
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                if self.state != 'HUB': self.return_to_hub()

    def draw(self):
        """Central draw delegation."""
        self.app.screen.fill(BG_COLOR)
        
        if self.state == 'HUB':
            self.draw_info()
            self.draw_hub()
        elif self.state == 'PLAYER_SETTINGS':
            self.player_menu.draw(self.app.screen)
        elif self.state == 'GARAGE':
            self.garage_menu.draw(self.app.screen)
        else:
            self.draw_placeholder(self.state)

    def draw_info(self):
        """Draws top status bar."""
        w = self.app.screen.get_width()
        pg.draw.rect(self.app.screen, PANEL_BG, (0,0,w,60))
        pg.draw.line(self.app.screen, ACCENT_BLUE, (0,60), (w,60), 2)
        f = pg.font.SysFont('Consolas', 24)
        
        ns = f.render(f"{self.app.lang.get('info_driver')}: {self.player.name}", True, TEXT_MAIN)
        self.app.screen.blit(ns, (20, 18))
        ms = f.render(f"${self.player.money}", True, ACCENT_GOLD)
        self.app.screen.blit(ms, ms.get_rect(topright=(w-20, 18)))

    def draw_hub(self):
        """Draws Hub specific elements."""
        for b in self.buttons: b.draw(self.app.screen)
        
        # Draw CURRENT CAR Preview on the left
        if self.player.current_car:
            sprite = get_car_sprite(self.app.assets, self.player.current_car)
            if sprite:
                # Scale up for display
                scaled = pg.transform.scale(sprite, (160, 160))
                # Position on the left side
                self.app.screen.blit(scaled, (100, 250))
                
                # Draw label "Current Ride"
                f = pg.font.SysFont('Consolas', 20)
                lbl = f.render(self.app.lang.get("lbl_current_car"), True, TEXT_DIM)
                self.app.screen.blit(lbl, (120, 420))
                
                # Draw Car Name
                name_s = pg.font.SysFont('Consolas', 24, bold=True).render(self.player.current_car, True, TEXT_MAIN)
                self.app.screen.blit(name_s, name_s.get_rect(center=(180, 450)))

    def draw_placeholder(self, txt):
        s = pg.font.SysFont('Consolas',32,bold=True).render(txt,True,TEXT_DIM)
        self.app.screen.blit(s, s.get_rect(center=(self.app.screen.get_width()//2, self.app.screen.get_height()//2)))