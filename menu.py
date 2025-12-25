import pygame as pg
from constants import *

class Button:
    def __init__(self, text, index, action, custom_color=None):
        self.text = text
        self.action = action
        
        # Font settings
        self.font_size = 35
        self.font = pg.font.SysFont('Consolas', self.font_size, bold=True)
        
        # Colors
        self.color_idle = custom_color if custom_color else BUTTON_COLOR
        self.color_hover = BUTTON_HOVER_COLOR
        self.text_color = TEXT_MAIN
        self.border_color = TEXT_DIM
        
        # Size calculation
        text_width, text_height = self.font.size(self.text)
        padding_x, padding_y = 30, 15
        self.width = text_width + padding_x
        self.height = text_height + padding_y
        
        # Positioning
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, start_y + index * (self.height + 20))
        
        # Shadow rect
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.x += 3
        self.shadow_rect.y += 3

        # Prerender text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.color_hover if is_hovered else self.color_idle
        
        # Draw shadow, body, border
        pg.draw.rect(screen, (15, 15, 20), self.shadow_rect, border_radius=8)
        pg.draw.rect(screen, current_color, self.rect, border_radius=8)
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Menu:
    def __init__(self, main_app):
        self.app = main_app
        self.state = "main"
        self.buttons = []
        self.title_font = pg.font.SysFont('Consolas', 60, bold=True)
        self.init_main_menu()

    def init_main_menu(self):
        """Initializes buttons for the main menu."""
        self.state = "main"
        self.buttons = [
            Button("PLAY", 0, self.go_to_saves),
            Button("OPTIONS", 1, lambda: print("Options clicked")),
            Button("EXIT", 2, self.app.quit_game, custom_color=ACCENT_RED)
        ]

    def init_save_menu(self):
        """Initializes buttons for save slot selection."""
        self.state = "saves"
        self.buttons = []
        
        # Check slots status
        slots_status = self.app.data_manager.check_save_slots()
        
        for i in range(1, 4):
            is_occupied = slots_status[i]
            
            # Text and Color logic
            if is_occupied:
                btn_text = f"SLOT {i} [LOAD GAME]"
                color = ACCENT_BLUE  # Blue for Load
            else:
                btn_text = f"SLOT {i} [NEW GAME]"
                color = ACCENT_GREEN # Green for New
            
            # Lambda to capture current index 'i'
            action = lambda slot=i: self.app.start_game_session(slot)
            
            self.buttons.append(Button(btn_text, i-1, action, custom_color=color))
            
        # Back button
        self.buttons.append(Button("BACK", 3, self.init_main_menu))

    def go_to_saves(self):
        self.init_save_menu()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Draw Title
        title_text = "SELECT SLOT" if self.state == "saves" else "CA RACING"
        title_surf = self.title_font.render(title_text, True, TEXT_MAIN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Draw Buttons
        for btn in self.buttons:
            btn.draw(screen)