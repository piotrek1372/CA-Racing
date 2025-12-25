import pygame as pg
import sys
from constants import *
from load_data import Data
from load_assets import load_game_assets
from menu import Menu
from player import Player

class GameSession:
    """
    Manages the active gameplay state (Garage, Race, etc.).
    """
    def __init__(self, screen, data_manager, slot_id, assets):
        self.screen = screen
        self.data_manager = data_manager
        self.slot_id = slot_id
        self.assets = assets
        
        # 1. Load raw JSON data
        self.game_db = self.data_manager.load_game_data()
        self.player_save_data = self.data_manager.load_player_state(slot_id)
        
        # 2. Initialize Player Object
        self.player = Player(self.player_save_data, self.game_db)
        
        # UI Resources
        self.font_ui = pg.font.SysFont('Consolas', 24)
        self.font_header = pg.font.SysFont('Consolas', 32, bold=True)
        
        print(f"[GAME] Session started. Player: {self.player.name}, Money: {self.player.money}")

    def update(self, events):
        """Handle gameplay logic updates."""
        # For now, just a placeholder for future logic (e.g. physics, race loop)
        pass

    def draw(self):
        """Render the game screen (Garage View for now)."""
        self.screen.fill(BG_COLOR)
        
        # --- DRAW UI HUD ---
        
        # 1. Header (Slot Info)
        header_text = f"GARAGE - SAVE SLOT {self.slot_id}"
        header_surf = self.font_header.render(header_text, True, ACCENT_BLUE)
        self.screen.blit(header_surf, (20, 20))
        
        # 2. Player Info Panel
        info_x, info_y = 20, 80
        
        # Helper to draw text lines
        stats = [
            f"DRIVER: {self.player.name}",
            f"LEVEL:  {self.player.level}",
            f"MONEY:  ${self.player.money}",
            f"CARS:   {len(self.player.garage)}"
        ]
        
        for i, line in enumerate(stats):
            color = ACCENT_GREEN if "$" in line else TEXT_MAIN
            surf = self.font_ui.render(line, True, color)
            self.screen.blit(surf, (info_x, info_y + i * 35))

        # 3. Visual separator
        pg.draw.line(self.screen, TEXT_DIM, (20, 240), (SCREEN_WIDTH - 20, 240), 2)

        # 4. Content Area (Placeholder for Car display)
        content_text = "PRESS [ESC] TO SAVE & QUIT TO MENU"
        content_surf = self.font_ui.render(content_text, True, ACCENT_RED)
        self.screen.blit(content_surf, (20, SCREEN_HEIGHT - 50))
        
        # Example: Draw car sprite if available
        if 'cars' in self.assets and self.assets['cars']:
            # Drawing a part of the sprite sheet as a test
            self.screen.blit(self.assets['cars'], (300, 100), (0, 0, 64, 64))

class Main:
    def __init__(self):
        pg.init()
        # Initialize display
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        
        # App State
        self.state = 'MENU'
        
        # Managers
        self.data_manager = Data()
        self.assets = load_game_assets()
        
        # Components
        self.menu = Menu(self)
        self.game_session = None

    def start_game_session(self, slot_id):
        """
        Handles the logic for both NEW GAME and LOAD GAME.
        """
        print(f"[MAIN] Attempting to start slot {slot_id}...")
        
        # 1. Check if save exists. If not, create it (New Game logic)
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            print(f"[MAIN] Save not found. Creating new save for Slot {slot_id}...")
            if not self.data_manager.create_new_save(slot_id):
                print("[MAIN] Critical Error: Failed to create save.")
                return

        # 2. Initialize Game Session (Load Game logic)
        # At this point, the file physically exists, so we can load it.
        try:
            self.game_session = GameSession(self.screen, self.data_manager, slot_id, self.assets)
            self.state = 'GAME'
        except Exception as e:
            print(f"[MAIN] Error loading game session: {e}")
            # Optionally show an error message on screen here

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            
            # Global Event Loop
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                
                # Global Keybinds
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.state == 'GAME':
                            # Return to Menu
                            self.state = 'MENU'
                            self.game_session = None 
                            self.menu.init_main_menu()

            # Update & Draw based on State
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