import pygame as pg
from constants import *

class Button:
    """
    A customizable UI Button with hover effects and cached text rendering.
    """
    def __init__(self, text, center_pos, action, custom_color=None):
        """
        :param text: Text to display.
        :param center_pos: Tuple (x, y) for the center of the button.
        :param action: Callback function to execute on click.
        :param custom_color: Optional override for the idle button color.
        """
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
        
        # Size calculation (Calculate once for performance)
        text_width, text_height = self.font.size(self.text)
        padding_x, padding_y = 30, 15
        self.width = text_width + padding_x
        self.height = text_height + padding_y
        
        # Positioning
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = center_pos
        
        # Shadow rect (Visual depth)
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.x += 3
        self.shadow_rect.y += 3

        # Prerender text surface (Optimization)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Renders the button to the screen."""
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.color_hover if is_hovered else self.color_idle
        
        # Draw shadow, body, and border
        pg.draw.rect(screen, (15, 15, 20), self.shadow_rect, border_radius=8)
        pg.draw.rect(screen, current_color, self.rect, border_radius=8)
        pg.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)
        
        # Blit the cached text surface
        screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        """Handles mouse clicks."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Menu:
    """
    Manages the Main Menu and Save Selection screens.
    """
    def __init__(self, main_app):
        self.app = main_app
        self.state = "main" # 'main' or 'saves'
        self.buttons = []
        
        # Font for the main title
        self.title_font = pg.font.SysFont('Consolas', 60, bold=True)
        
        # Initialize the default view
        self.init_main_menu()

    def init_main_menu(self):
        """Sets up buttons for the Main Menu."""
        self.state = "main"
        self.buttons = []
        
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        gap_y = 70

        # Define buttons configuration
        options = [
            ("PLAY", self.go_to_saves, None),
            ("OPTIONS", lambda: print("Options clicked (TODO)"), None),
            ("EXIT", self.app.quit_game, ACCENT_RED)
        ]

        # Create Button objects
        for i, (text, action, color) in enumerate(options):
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(text, pos, action, custom_color=color))

    def init_save_menu(self):
        """Sets up buttons for Save Slot selection."""
        self.state = "saves"
        self.buttons = []
        
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        gap_y = 80
        
        # Fetch slot status from Data Manager
        slots_status = self.app.data_manager.check_save_slots()
        
        for i in range(1, 4):
            is_occupied = slots_status[i]
            
            # Text and Color logic based on save state
            if is_occupied:
                btn_text = f"SLOT {i} [LOAD GAME]"
                color = ACCENT_BLUE
            else:
                btn_text = f"SLOT {i} [NEW GAME]"
                color = ACCENT_GREEN
            
            # Lambda to capture current index 'i'
            action = lambda slot=i: self.app.start_game_session(slot)
            
            pos = (center_x, start_y + (i-1) * gap_y)
            self.buttons.append(Button(btn_text, pos, action, custom_color=color))
            
        # Back button
        back_pos = (center_x, start_y + 3 * gap_y + 20)
        self.buttons.append(Button("BACK", back_pos, self.init_main_menu))

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
        
        # Draw all buttons
        for btn in self.buttons:
            btn.draw(screen)