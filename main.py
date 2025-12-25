import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import load_game_assets
from menu import Menu, Button # Import Button to use inside GameSession
from player import Player

class GameSession:
    """
    Manages the active gameplay session.
    Controls the in-game 'Hub' menu (Race, Garage, Shop, Settings).
    """
    def __init__(self, main_app, slot_id):
        self.app = main_app
        self.slot_id = slot_id
        
        # Shortcuts for app resources
        self.screen = main_app.screen
        self.assets = main_app.assets
        self.data_manager = main_app.data_manager
        
        # Load Game Data
        self.game_db = self.data_manager.load_game_data()
        self.player_save_data = self.data_manager.load_player_state(slot_id)
        self.player = Player(self.player_save_data, self.game_db)
        
        # Fonts
        self.font_header = pg.font.SysFont('Consolas', 32, bold=True)
        self.font_ui = pg.font.SysFont('Consolas', 24)
        
        # Session State: 'HUB', 'RACE', 'GARAGE', 'SHOP', 'SETTINGS'
        self.state = 'HUB'
        
        # Initialize UI Buttons for the Hub
        self.buttons = []
        self.init_hub_ui()
        
        print(f"[GAME] Session started. Player: {self.player.name}")

    def init_hub_ui(self):
        """Creates the buttons for the main Game Menu."""
        self.buttons = []
        
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        gap_y = 70
        
        # Menu Options
        options = [
            ("RACE", lambda: self.change_state('RACE'), ACCENT_GREEN),
            ("GARAGE", lambda: self.change_state('GARAGE'), None),
            ("SHOP", lambda: self.change_state('SHOP'), None),
            ("SETTINGS", lambda: self.change_state('SETTINGS'), None),
            ("MAIN MENU", self.exit_to_main_menu, ACCENT_RED)
        ]
        
        for i, (text, action, color) in enumerate(options):
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(text, pos, action, custom_color=color))

    def change_state(self, new_state):
        """Switches the internal session state."""
        print(f"[GAME] Switching state: {self.state} -> {new_state}")
        self.state = new_state
        # Here you could initialize specific UIs for Garage/Shop in the future

    def exit_to_main_menu(self):
        """Closes the session and returns to the App's Main Menu."""
        # Optional: Save game here before exiting
        # self.data_manager.save_player_state(self.slot_id, self.player.to_dict()) 
        self.app.close_game_session()

    def update(self, events):
        """Handles updates based on current internal state."""
        
        # Handle Button clicks if in HUB state
        if self.state == 'HUB':
            for event in events:
                for btn in self.buttons:
                    btn.handle_event(event)
        
        # Global Session Inputs (e.g. ESC to go back)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.state != 'HUB':
                        self.change_state('HUB') # Return to Hub from sub-menus

    def draw(self):
        """Renders the game screen."""
        self.screen.fill(BG_COLOR)
        
        # Draw Top Bar (Player Info)
        self.draw_player_info()
        
        if self.state == 'HUB':
            self.draw_hub()
        elif self.state == 'RACE':
            self.draw_placeholder("RACE MODE (Under Construction)")
        elif self.state == 'GARAGE':
            self.draw_placeholder("GARAGE VIEW (Under Construction)")
        elif self.state == 'SHOP':
            self.draw_placeholder("ITEM SHOP (Under Construction)")
        elif self.state == 'SETTINGS':
            self.draw_placeholder("GAME SETTINGS (Under Construction)")

    def draw_player_info(self):
        """Draws the HUD at the top."""
        # Background bar for HUD
        pg.draw.rect(self.screen, PANEL_BG, (0, 0, SCREEN_WIDTH, 60))
        pg.draw.line(self.screen, ACCENT_BLUE, (0, 60), (SCREEN_WIDTH, 60), 2)
        
        # Player Name
        name_surf = self.font_ui.render(f"DRIVER: {self.player.name}", True, TEXT_MAIN)
        self.screen.blit(name_surf, (20, 18))
        
        # Money (Right aligned)
        money_text = f"${self.player.money}"
        money_surf = self.font_ui.render(money_text, True, ACCENT_GOLD)
        money_rect = money_surf.get_rect(topright=(SCREEN_WIDTH - 20, 18))
        self.screen.blit(money_surf, money_rect)

    def draw_hub(self):
        """Draws the Hub menu buttons."""
        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        # Draw Car Visualization (e.g. center or side)
        # Using the assets loaded in Main
        if 'cars' in self.assets and self.assets['cars']:
            # Scale up the car for the menu display (64x64 -> 128x128)
            car_sprite = self.assets['cars'].subsurface((0, 0, 64, 64)) # Assuming 1st car
            car_scaled = pg.transform.scale(car_sprite, (128, 128))
            
            # Position it nicely (e.g., left of the menu or top)
            # For now, let's put it on the left side
            self.screen.blit(car_scaled, (100, 250))

    def draw_placeholder(self, text):
        """Helper to draw placeholder screens."""
        text_surf = self.font_header.render(text, True, TEXT_DIM)
        rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text_surf, rect)
        
        info_surf = self.font_ui.render("Press ESC to return", True, TEXT_MAIN)
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(info_surf, info_rect)


class Main:
    def __init__(self):
        pg.init()
        # Initialize Window
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        
        # App State: 'MENU' or 'GAME'
        self.state = 'MENU'
        
        # Load Resources
        # Note: Ensure load_assets returns a valid dictionary even if empty
        try:
            self.assets = load_game_assets()
        except Exception as e:
            print(f"[MAIN] Warning: Failed to load assets: {e}")
            self.assets = {}
            
        self.data_manager = Data()
        
        # Initialize Main Menu
        self.menu = Menu(self)
        
        # Game Session Placeholder
        self.game_session = None

    def start_game_session(self, slot_id):
        """Starts a game session from the given save slot."""
        print(f"[MAIN] Loading Slot {slot_id}...")
        
        # Ensure save exists
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            print(f"[MAIN] Creating new save for Slot {slot_id}...")
            if not self.data_manager.create_new_save(slot_id):
                return # Error creating save

        # Initialize Session
        try:
            self.game_session = GameSession(self, slot_id)
            self.state = 'GAME'
        except Exception as e:
            print(f"[MAIN] Error starting game session: {e}")

    def close_game_session(self):
        """Ends the current game session and returns to Main Menu."""
        print("[MAIN] Closing session...")
        self.game_session = None
        self.state = 'MENU'
        self.menu.init_main_menu()

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            
            # Global Events
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
            
            # State Machine Update/Draw
            if self.state == 'MENU':
                self.menu.update(events[0] if events else pg.event.Event(pg.USEREVENT)) 
                # Note: menu.update iterates over all buttons internally with the event loop
                # Ideally, we pass the loop to update or handle events inside update.
                # Let's fix this slightly: pass the whole event list or iterate outside.
                # FIX: Menu.update expects a single event in the current implementation.
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