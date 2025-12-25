import pygame as pg
from constants import *
# Upewnij się, że importujesz zoptymalizowaną klasę Button z poprzedniej rozmowy!
# Jeśli jej nie masz w pliku, wklej tutaj klasę Button z cache'owaniem tekstu.

class Button:
    # ... (Wklej tutaj zoptymalizowaną klasę Button z poprzedniej odpowiedzi) ...
    # Dla skrótu zakładam, że ją masz. Jeśli nie - daj znać.
    def __init__(self, text, index, action):
        self.text = text
        self.action = action
        self.font_size = 35
        self.font = pg.font.SysFont('Consolas', self.font_size, bold=True)
        self.color_idle = BUTTON_COLOR
        self.color_hover = BUTTON_HOVER_COLOR
        self.text_color = TEXT_MAIN
        self.border_color = TEXT_DIM
        
        # Optymalizacja rozmiaru
        text_width, text_height = self.font.size(self.text)
        self.width = text_width + 40
        self.height = text_height + 20
        self.topleft = (SCREEN_WIDTH / 2 - self.width / 2, index * (self.height + 15) + 150)
        self.rect = pg.Rect(self.topleft[0], self.topleft[1], self.width, self.height)
        
        # Prerenderowanie tekstu
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.color_hover if is_hovered else self.color_idle
        
        pg.draw.rect(screen, current_color, self.rect, border_radius=5)
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Menu:
    def __init__(self, game_instance):
        self.game = game_instance
        self.state = "main" # main, saves
        self.buttons = []
        self.create_main_menu()

    def create_main_menu(self):
        """Tworzy przyciski menu głównego"""
        self.state = "main"
        self.buttons = [
            Button("Nowa Gra", 0, self.go_to_saves),
            Button("Opcje", 1, lambda: print("Opcje - todo")),
            Button("Wyjście", 2, self.game.quit_game)
        ]

    def create_save_menu(self):
        """Tworzy menu wyboru slotów dynamicznie"""
        self.state = "saves"
        self.buttons = []
        
        # Pobierz status slotów z DataManagera
        slots = self.game.data_manager.check_save_slots()
        
        for i in range(1, 4):
            is_taken = slots[i]
            text = f"Slot {i} [{'ZAJĘTY' if is_taken else 'WOLNY'}]"
            # Funkcja lambda z 'default argument' (idx=i) żeby zapamiętać wartość i
            action = lambda idx=i: self.game.start_new_game(idx)
            
            btn = Button(text, i-1, action)
            # Jeśli zajęty, zmieniamy kolor na np. czerwonawy/złoty (opcjonalnie)
            if is_taken:
                btn.text_color = ACCENT_GOLD
                btn.update_text(text) # Przerysowanie
                
            self.buttons.append(btn)
            
        # Przycisk powrotu
        self.buttons.append(Button("Powrót", 3, self.create_main_menu))

    def go_to_saves(self):
        self.create_save_menu()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Tytuł (można zoptymalizować wrzucając do init)
        title_font = pg.font.SysFont('Consolas', 60, bold=True)
        title_text = "WYBÓR ZAPISU" if self.state == "saves" else "CA RACING"
        title_surf = title_font.render(title_text, True, ACCENT_BLUE)
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        for btn in self.buttons:
            btn.draw(screen)
            
    # Metoda pomocnicza do Button.update_text (trzeba dodać do klasy Button)
    # Wklej to do klasy Button:
    # def update_text(self, new_text):
    #     self.text = new_text
    #     self.text_surf = self.font.render(self.text, True, self.text_color)
    #     self.text_rect = self.text_surf.get_rect(center=self.rect.center)