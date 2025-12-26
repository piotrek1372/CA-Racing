import pygame as pg
from constants import *
from menu import Button

class SettingsMenu:
    """
    Unified Settings Menu with functional logic for Graphics, Audio, and Language.
    """
    def __init__(self, app, return_callback):
        self.app = app
        self.return_callback = return_callback
        self.screen = app.screen
        self.current_state = 'MAIN'
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.buttons = []
        
        self.init_main_view()

    def _get_center(self):
        """Helper to get current center even if resolution changed."""
        w, h = self.app.screen.get_size()
        return w // 2

    def init_main_view(self):
        self.current_state = 'MAIN'
        self.buttons = []
        center_x = self._get_center()
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
        self.current_state = 'AUDIO'
        self.buttons = []
        center_x = self._get_center()
        start_y = 250
        
        # Placeholder functionality for Audio
        self.buttons.append(Button(f"{self.app.lang.get('audio_sfx')}: 100%", (center_x, start_y), lambda: print("SFX TODO")))
        self.buttons.append(Button(f"{self.app.lang.get('audio_music')}: 100%", (center_x, start_y + 70), lambda: print("Music TODO")))
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + 160), self.init_main_view, ACCENT_RED))

    def init_graphics_view(self):
        """
        Creates functional buttons for graphics settings.
        Reads current state from app.player.settings (if in game) or uses defaults.
        """
        self.current_state = 'GRAPHICS'
        self.buttons = []
        center_x = self._get_center()
        start_y = 150
        gap_y = 70
        
        # We need access to player settings. If loaded from Main Menu without a save loaded,
        # we might need a temporary settings holder. For now, assuming Global Main has settings
        # or we edit the currently active session's player.
        
        # If we are in Main Menu (no game session), we edit 'global' app settings
        # stored in app.temp_settings, otherwise app.game_session.player.settings
        
        current_settings = self._get_active_settings()

        # 1. Resolution
        res_idx = current_settings.get("resolution_idx", 0)
        if res_idx < len(RESOLUTIONS):
            curr_res = RESOLUTIONS[res_idx]
        else:
            curr_res = RESOLUTIONS[0]
        
        res_text = f"{self.app.lang.get('gfx_resolution')}: {curr_res[0]}x{curr_res[1]}"
        self.buttons.append(Button(res_text, (center_x, start_y), self.cycle_resolution))

        # 2. Fullscreen
        is_fs = current_settings.get("fullscreen", False)
        fs_status = self.app.lang.get("val_on") if is_fs else self.app.lang.get("val_off")
        fs_text = f"{self.app.lang.get('gfx_fullscreen')}: {fs_status}"
        self.buttons.append(Button(fs_text, (center_x, start_y + gap_y), self.toggle_fullscreen))

        # 3. FPS
        fps_val = current_settings.get("max_fps", 60)
        fps_text = f"{self.app.lang.get('gfx_fps')}: {fps_val}"
        self.buttons.append(Button(fps_text, (center_x, start_y + gap_y*2), self.cycle_fps))

        # 4. Quality
        qual_val = current_settings.get("quality", "HIGH")
        # Map internal code to localized string
        q_map = {
            "LOW": self.app.lang.get("quality_low"),
            "MED": self.app.lang.get("quality_med"),
            "HIGH": self.app.lang.get("quality_high")
        }
        qual_text = f"{self.app.lang.get('gfx_quality')}: {q_map.get(qual_val, qual_val)}"
        self.buttons.append(Button(qual_text, (center_x, start_y + gap_y*3), self.cycle_quality))

        # Back
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + gap_y*5), self.init_main_view, ACCENT_RED))

    # --- Logic Helpers ---

    def _get_active_settings(self):
        """Returns the dictionary to modify (Player's or App's temp)."""
        if self.app.game_session:
            return self.app.game_session.player.settings
        else:
            return self.app.global_settings

    def _save_and_apply(self):
        """Refreshes the view (to show new text) and applies graphics."""
        self.app.apply_graphics_settings() # Apply window changes
        self.init_graphics_view() # Re-create buttons with new text/positions

    def cycle_resolution(self):
        settings = self._get_active_settings()
        idx = settings.get("resolution_idx", 0)
        idx = (idx + 1) % len(RESOLUTIONS)
        settings["resolution_idx"] = idx
        self._save_and_apply()

    def toggle_fullscreen(self):
        settings = self._get_active_settings()
        settings["fullscreen"] = not settings.get("fullscreen", False)
        self._save_and_apply()

    def cycle_fps(self):
        settings = self._get_active_settings()
        current = settings.get("max_fps", 60)
        # Find next in list
        try:
            curr_idx = FPS_LIMITS.index(current)
            next_idx = (curr_idx + 1) % len(FPS_LIMITS)
        except ValueError:
            next_idx = 1 # Default to 60 if weird value
        
        settings["max_fps"] = FPS_LIMITS[next_idx]
        self._save_and_apply()

    def cycle_quality(self):
        settings = self._get_active_settings()
        modes = ["LOW", "MED", "HIGH"]
        current = settings.get("quality", "HIGH")
        try:
            curr_idx = modes.index(current)
            next_idx = (curr_idx + 1) % len(modes)
        except ValueError:
            next_idx = 2
        
        settings["quality"] = modes[next_idx]
        # Quality might affect asset loading, which is complex to do runtime,
        # but we can affect drawing logic immediately.
        self._save_and_apply()

    def init_language_view(self):
        self.current_state = 'LANGUAGE'
        self.buttons = []
        center_x = self._get_center()
        start_y = 200
        gap_y = 60
        
        langs = [("English", "en"), ("Polski", "pl"), ("Deutsch", "de"), 
                 ("Español", "es"), ("Français", "fr"), ("Português", "pt")]
        
        for i, (name, code) in enumerate(langs):
            action = lambda c=code: self.change_language(c)
            pos = (center_x, start_y + i * gap_y)
            self.buttons.append(Button(name, pos, action))
            
        self.buttons.append(Button(self.app.lang.get("menu_back"), (center_x, start_y + len(langs)*gap_y + 20), self.init_main_view, ACCENT_RED))

    def change_language(self, code):
        self.app.lang.load_language(code)
        self.init_language_view()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        title_key = "settings_title"
        if self.current_state == 'AUDIO': title_key = "settings_audio"
        elif self.current_state == 'GRAPHICS': title_key = "settings_graphics"
        elif self.current_state == 'LANGUAGE': title_key = "settings_language"
        
        title_text = self.app.lang.get(title_key)
        title_surf = self.title_font.render(title_text, True, TEXT_MAIN)
        title_rect = title_surf.get_rect(center=(self._get_center(), 100))
        screen.blit(title_surf, title_rect)
        
        for btn in self.buttons:
            btn.draw(screen)