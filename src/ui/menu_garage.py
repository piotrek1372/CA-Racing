import pygame as pg
from src.constants import *
from src.ui.widgets import Button
from src.core.assets import get_car_sprite

class GarageMenu:
    """
    Displays the player's garage allowing them to select an active car.
    Visualize cars in a grid system.
    """
    def __init__(self, app, player, return_callback):
        self.app = app
        self.player = player
        self.return_callback = return_callback
        self.screen = app.screen
        
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.info_font = pg.font.SysFont('Consolas', 24)
        
        # List of tuples: (pg.Rect, car_id_string)
        self.car_rects = [] 
        self.buttons = []
        
        self.init_ui()

    def init_ui(self):
        """Initializes buttons and calculates car grid positions."""
        self.buttons = []
        cx = self.app.screen.get_width() // 2
        h = self.app.screen.get_height()
        
        # Back button at the bottom
        self.buttons.append(Button(
            self.app.lang.get("menu_back"), 
            (cx, h - 80), 
            self._on_back, 
            app=self.app, 
            custom_color=ACCENT_RED
        ))
        
        # Calculate grid for cars
        self.calculate_car_grid()

    def calculate_car_grid(self):
        """Calculates positions for owned cars to display in a grid layout."""
        self.car_rects = []
        
        # Layout settings
        start_x = 150
        start_y = 180
        gap_x = 220
        gap_y = 200
        cols_per_row = 4
        
        for i, item in enumerate(self.player.garage):
            # FIX: Ensure we have the String ID, even if item is a Dict object
            # Check model_id first (correct for new saves), then name
            car_id = item
            if isinstance(item, dict):
                car_id = item.get('model_id') or item.get('name')
            
            row = i // cols_per_row
            col = i % cols_per_row
            
            x = start_x + col * gap_x
            y = start_y + row * gap_y
            
            # Target size for background panel
            rect = pg.Rect(x, y, 160, 160)
            self.car_rects.append((rect, car_id))

    def _on_back(self):
        self.app.audio.play_sfx('ui_back')
        self.return_callback()

    def handle_click(self, mouse_pos):
        """Checks if a car slot was clicked."""
        for rect, car_id in self.car_rects:
            if rect.collidepoint(mouse_pos):
                if self.player.set_current_car(car_id):
                    self.app.audio.play_sfx('ui_select')
                else:
                    self.app.audio.play_sfx('ui_error')
                return

    def update(self, event):
        """Handles input events."""
        for btn in self.buttons:
            btn.handle_event(event)
            
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def draw(self, screen):
        """Draws the garage menu."""
        screen.fill(BG_COLOR)
        
        # Title
        title_surf = self.title_font.render(self.app.lang.get("title_garage"), True, TEXT_MAIN)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 70))
        screen.blit(title_surf, title_rect)
        
        # Draw Cars Grid
        mouse_pos = pg.mouse.get_pos()
        
        for rect, car_id in self.car_rects:
            # 1. Get Sprite (Now safely handled in assets.py even if passed dict by mistake, 
            # though calculate_car_grid tries to pass string)
            sprite = get_car_sprite(self.app.assets, car_id)
            
            # 2. Determine state (Selected vs Hovered vs Idle)
            is_selected = (car_id == self.player.current_car)
            is_hovered = rect.collidepoint(mouse_pos)
            
            # 3. Draw Background
            bg_color = (60, 60, 70)
            if is_selected:
                bg_color = (40, 70, 40) # Greenish tint
            elif is_hovered:
                bg_color = (70, 70, 80) # Lighter
                
            pg.draw.rect(screen, bg_color, rect, border_radius=10)
            
            # 4. Draw Border
            border_col = TEXT_DIM
            width = 2
            if is_selected:
                border_col = ACCENT_GOLD
                width = 4
            elif is_hovered:
                border_col = TEXT_MAIN
            
            pg.draw.rect(screen, border_col, rect, width, border_radius=10)

            # 5. Draw "Selected" Label if active
            if is_selected:
                sel_surf = self.info_font.render(self.app.lang.get("lbl_selected"), True, ACCENT_GOLD)
                sel_rect = sel_surf.get_rect(midbottom=(rect.centerx, rect.top - 5))
                screen.blit(sel_surf, sel_rect)

            # 6. Draw Scaled Sprite
            if sprite:
                target_size = (128, 128) 
                scaled = pg.transform.scale(sprite, target_size)
                img_rect = scaled.get_rect(center=rect.center)
                screen.blit(scaled, img_rect)
                
            # 7. Draw Name
            # Ensure we display string name
            name_surf = self.info_font.render(str(car_id), True, TEXT_DIM)
            name_rect = name_surf.get_rect(midtop=(rect.centerx, rect.bottom + 8))
            screen.blit(name_surf, name_rect)

        # Draw UI Buttons
        for btn in self.buttons:
            btn.draw(screen)