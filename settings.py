import pygame as pg
from constants import *
from menu import Button  # Reusing the Button class for consistency

class SettingsMenu:
    """
    Unified Settings Menu accessible from both Main Menu and In-Game Hub.
    Handles sub-menus for Audio, Graphics, and Language.
    """
    def __init__(self, app, return_callback):
        """
        :param app: Reference to the main application instance (for language access).
        :param return_callback: Function to call when 'Back' is pressed (restores previous state).
        """
        self.app = app
        self.return_callback = return_callback
        self.screen = app.screen
        
        # Internal state: 'MAIN', 'AUDIO', 'GRAPHICS', 'LANGUAGE'
        self.current_state = 'MAIN'
        
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.buttons = []
        
        # Initialize the main settings view
        self.init_main_view()

    def init_main_view(self):
        """Creates buttons for the top-level settings menu."""
        self.current_state = 'MAIN'
        self.buttons = []
        
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        gap_y = 70
        
        options = [
            (self.app.lang.get("settings_audio"), lambda: self.init_audio_view()),
            (self.app.lang.get("settings_graphics"), lambda: self.init_graphics_view()),
            (self.app.lang.get("settings_language"), lambda: self.init_language_view()),
            (self.app.lang.get("menu_back"), self.return_callback, ACCENT_RED)
        ]
        
        for i, item in enumerate(options):
            text, action = item[0], item[1]
            color = item[2] if len(item) > 2 else None
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(text, pos, action, custom_color=color))

    def init_audio_view(self):
        """Creates buttons for Audio settings."""
        self.current_state = 'AUDIO'
        self.buttons = []
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        
        # Placeholders for sliders/toggles
        # In a real implementation, these would be interactive sliders
        self.buttons.append(Button(f"{self.app.lang.get('audio_sfx')}: 100%", (center_x, start_y), lambda: print("SFX Change")))
        self.buttons.append(Button(f"{self.app.lang.get('audio_music')}: 100%", (center_x, start_y + 70), lambda: print("Music Change")))
        
        # Back button returns to Settings Main View
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + 160), self.init_main_view, ACCENT_RED))

    def init_graphics_view(self):
        """Creates buttons for Graphics settings."""
        self.current_state = 'GRAPHICS'
        self.buttons = []
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        
        self.buttons.append(Button(f"{self.app.lang.get('gfx_fps')}: 60", (center_x, start_y), lambda: print("FPS Change")))
        self.buttons.append(Button(f"{self.app.lang.get('gfx_quality')}: HIGH", (center_x, start_y + 70), lambda: print("Quality Change")))
        
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + 160), self.init_main_view, ACCENT_RED))

    def init_language_view(self):
        """Creates buttons for Language selection."""
        self.current_state = 'LANGUAGE'
        self.buttons = []
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        gap_y = 60
        
        # Available languages
        langs = [("English", "en"), ("Polski", "pl"), ("Deutsch", "de"), 
                 ("Español", "es"), ("Français", "fr"), ("Português", "pt")]
        
        for i, (name, code) in enumerate(langs):
            # Action: change language and refresh the view immediately
            action = lambda c=code: self.change_language(c)
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(name, pos, action))
            
        # Back button
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + len(langs)*gap_y + 20), self.init_main_view, ACCENT_RED))

    def change_language(self, code):
        """Updates the language and refreshes the current view."""
        print(f"[SETTINGS] Changing language to {code}")
        self.app.lang.load_language(code)
        # Re-initialize the language view to update texts (e.g. Back button)
        self.init_language_view()

    def update(self, event):
        """Handles events for the active buttons."""
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        """Draws the settings menu."""
        screen.fill(BG_COLOR)
        
        # Draw Title
        title_key = "settings_title"
        if self.current_state == 'AUDIO': title_key = "settings_audio"
        elif self.current_state == 'GRAPHICS': title_key = "settings_graphics"
        elif self.current_state == 'LANGUAGE': title_key = "settings_language"
        
        title_text = self.app.lang.get(title_key)
        title_surf = self.title_font.render(title_text, True, TEXT_MAIN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Draw Buttons
        for btn in self.buttons:
            btn.draw(screen)