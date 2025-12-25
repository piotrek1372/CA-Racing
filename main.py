import pygame as pg
from constants import *
from menu import Menu
from load_assets import load_game_assets
from load_data import Data

class GameSession:
    def __init__(self, screen, data_manager, slot_id):
        self.screen = screen
        self.data_manager = data_manager
        self.slot_id = slot_id
        
        self.game_db = self.data_manager.load_game_data() # Baza przedmiotów
        self.player_state = self.data_manager.load_player_state(slot_id) # Save gracza
        
        print(f"Załadowano grę na slocie {slot_id}. Gracz: {self.player_state['player']['name']}")

    def run(self):

        self.screen.fill(BG_COLOR)
        font = pg.font.SysFont('Consolas', 30)
        text = font.render(f"GRA W TOKU (Slot {self.slot_id}) - Wciśnij ESC aby wyjść", True, TEXT_MAIN)
        self.screen.blit(text, (50, 300))
        
        # Wyświetl stan kasy (test odczytu JSON)
        money = self.player_state['player']['money']
        money_text = font.render(f"Kasa: {money}$", True, ACCENT_GREEN)
        self.screen.blit(money_text, (50, 350))

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption("CA Racing")
        self.clock = pg.time.Clock()
        self.running = True
        self.state = "menu" # menu, game
        
        # 1. Ładowanie zasobów i narzędzi
        self.assets = load_game_assets()
        self.data_manager = Data()
        
        # 2. Inicjalizacja Menu
        self.menu = Menu(self)
        
        # 3. Placeholder na sesję gry
        self.current_session = None

    def start_new_game(self, slot_id):
        """Logika uruchamiana po wybraniu slotu w menu"""
        print(f"Wybrano slot {slot_id}")
        
        # 1. Jeśli save nie istnieje, stwórz go
        slots = self.data_manager.check_save_slots()
        if not slots[slot_id]:
            success = self.data_manager.create_new_save(slot_id)
            if not success:
                return # Błąd tworzenia

        # 2. Załaduj sesję gry
        self.current_session = GameSession(self.screen, self.data_manager, slot_id)
        
        # 3. Zmień stan
        self.state = "game"

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                
                # Obsługa inputu zależnie od stanu
                if self.state == "menu":
                    self.menu.update(event)
                elif self.state == "game":
                    # Tutaj obsługa inputu w grze (np. ESC wraca do menu)
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        self.state = "menu"
                        self.current_session = None # Czyścimy sesję (opcjonalne)

            # Rysowanie
            if self.state == "menu":
                self.menu.draw(self.screen)
            elif self.state == "game":
                if self.current_session:
                    self.current_session.run()

            pg.display.flip()
            self.clock.tick(FPS)

        pg.quit()

if __name__ == "__main__":
    app = Main()
    app.run()