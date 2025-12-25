import pygame as pg
import sys
from constants import *

# --- POPRAWKA IMPORTU ---
# Importujemy konkretną funkcję z pliku load_assets.py
from load_assets import load_game_assets
from load_data import Data
from menu import Menu
# from game import GameSession # Odkomentuj, gdy będziesz miał ten plik gotowy i działający
# Na razie używamy klasy GameSession zdefiniowanej lokalnie (jeśli taką masz) lub importujemy

# Jeśli GameSession jest w tym samym pliku co Main, zostaw tak.
# Jeśli przeniosłeś GameSession do game.py, dodaj: from game import GameSession

class GameSession:
    """Tymczasowa klasa sesji gry (lub zaimportowana z game.py)"""
    def __init__(self, screen, data_manager, slot_id, assets):
        self.screen = screen
        self.assets = assets
        self.slot_id = slot_id
        self.font = pg.font.SysFont('Consolas', 24)
        print(f"[GAME] Start sesji na slocie {slot_id}")

    def update(self, events):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        # Test wyświetlania mapy
        if 'maps' in self.assets and len(self.assets['maps']) > 0:
            self.screen.blit(self.assets['maps'][0], (0, 0))
        
        # Test wyświetlania auta
        if 'cars' in self.assets and self.assets['cars']:
            self.screen.blit(self.assets['cars'], (100, 100), (0,0,64,64))
            
        text = self.font.render(f"GRA W TOKU - SLOT {self.slot_id} (ESC - wyjście)", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

class Main:
    def __init__(self):
        pg.init()
        # 1. Najpierw tworzymy okno (Display)
        # Jest to KLUCZOWE dla działania load_assets (funkcje convert())
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        
        self.state = 'MENU'
        
        # 2. Dopiero teraz ładujemy assety
        try:
            self.assets = load_game_assets()
        except Exception as e:
            print(f"KRYTYCZNY BŁĄD ŁADOWANIA ZASOBÓW: {e}")
            self.assets = {} # Pusty słownik, żeby gra się nie wywaliła od razu

        # 3. Ładujemy dane
        self.data_manager = Data()
        
        # 4. Inicjalizujemy Menu
        self.menu = Menu(self)
        self.game_session = None

    def start_game_session(self, slot_id):
        # Sprawdź sloty
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            self.data_manager.create_new_save(slot_id)

        # Uruchom sesję
        self.game_session = GameSession(self.screen, self.data_manager, slot_id, self.assets)
        self.state = 'GAME'

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE and self.state == 'GAME':
                        self.state = 'MENU'
                        self.game_session = None
                        self.menu.init_main_menu()

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