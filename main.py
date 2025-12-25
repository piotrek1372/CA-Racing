import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import Assets
from menu import Menu

class GameSession:
    """
    Represents the active gameplay state (Garage, Race, etc.).
    Loaded after selecting a save slot.
    """
    def __init__(self, screen, data_manager, slot_id, assets):
        self.screen = screen
        self.data_manager = data_manager
        self.slot_id = slot_id
        self.assets = assets
        
        # Load data
        self.game_db = self.data_manager.load_game_data()
        self.player_state = self.data_manager.load_player_state(slot_id)
        
        self.font = pg.font.SysFont('Consolas', 24)
        print(f"[GAME] Session started on Slot {self.slot_id}")

    def update(self, events):
        """Handle gameplay logic."""
        pass

    def draw(self):
        """Render the game/garage screen."""
        self.screen.fill(BG_COLOR)
        
        # Debug/Info display
        p_name = self.player_state['player']['name']
        p_money = self.player_state['player']['money']
        
        info_lines = [
            f"Garage View (Slot {self.slot_id})",
            f"Player: {p_name}",
            f"Money: ${p_money}",
            "Press ESC to return to Menu"
        ]
        
        for i, line in enumerate(info_lines):
            surf = self.font.render(line, True, TEXT_MAIN)
            self.screen.blit(surf, (50, 50 + i * 30))

        # Example: Draw a car sprite if available
        if 'cars' in self.assets and self.assets['cars']:
            # Just drawing the whole spritesheet as a test
            self.screen.blit(self.assets['cars'], (50, 200))

class Main:
    def __init__(self):
        pg.init()
        # Initialize display with Double Buffering for performance
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        
        # App State: 'MENU' or 'GAME'
        self.state = 'MENU'
        
        # Initialize Managers
        self.data_manager = Data()
        self.assets = Assets() # Ensure this function returns a dict
        
        # Initialize Components
        self.menu = Menu(self)
        self.game_session = None

    def start_game_session(self, slot_id):
        """Transitions from Menu to Game using the specified save slot."""
        
        # check if save exists, if not create it
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            print(f"[MAIN] Creating new save for Slot {slot_id}...")
            if not self.data_manager.create_new_save(slot_id):
                print("[MAIN] Failed to create save.")
                return

        # Initialize session
        self.game_session = GameSession(self.screen, self.data_manager, slot_id, self.assets)
        self.state = 'GAME'

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            
            # Global Event Handling
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                
                # Global Keybinds
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.state == 'GAME':
                            self.state = 'MENU'
                            self.game_session = None # Unload session
                            self.menu.init_main_menu() # Reset menu

            # State Machine Update/Draw
            if self.state == 'MENU':
                # Pass events to menu
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