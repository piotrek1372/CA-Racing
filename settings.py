import pygame as pg
from constants import *
from menu import Button, InputBox

class GlobalSettingsMenu:
    """
    Handles Global Settings (Graphics, Audio, Language).
    Accessible ONLY from the Main Menu.
    Saves to data/settings.json via DataManager.
    """
    def __init__(self, app, return_callback):
        self.app = app
        self.return_callback = return_callback
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.buttons = []
        self.current_state = 'MAIN'
        self.init_main_view()

    def _get_center(self):
        return self.app.screen.get_width() // 2

    def init_main_view(self):
        self.current_state = 'MAIN'
        self.buttons = []
        cx = self._get_center()
        y = 250
        gap = 70
        
        opts = [
            (self.app.lang.get("settings_audio"), self.init_audio_view),
            (self.app.lang.get("settings_graphics"), self.init_graphics_view),
            (self.app.lang.get("settings_language"), self.init_language_view),
            (self.app.lang.get("menu_back"), self.return_callback, ACCENT_RED)
        ]
        
        for i, (txt, act, *col) in enumerate(opts):
            c = col[0] if col else None
            self.buttons.append(Button(txt, (cx, y + i*gap), act, custom_color=c))

    def init_graphics_view(self):
        self.current_state = 'GRAPHICS'
        self.buttons = []
        cx = self._get_center()
        y = 150
        gap = 70
        
        # Modify global settings directly
        gs = self.app.global_settings

        # Resolution
        res_idx = gs.get("resolution_idx", 0)
        curr_res = RESOLUTIONS[res_idx] if res_idx < len(RESOLUTIONS) else RESOLUTIONS[0]
        self.buttons.append(Button(f"{self.app.lang.get('gfx_resolution')}: {curr_res[0]}x{curr_res[1]}", (cx, y), self.cycle_resolution))

        # Fullscreen
        fs_txt = self.app.lang.get("val_on") if gs.get("fullscreen") else self.app.lang.get("val_off")
        self.buttons.append(Button(f"{self.app.lang.get('gfx_fullscreen')}: {fs_txt}", (cx, y+gap), self.toggle_fullscreen))

        # FPS
        self.buttons.append(Button(f"{self.app.lang.get('gfx_fps')}: {gs.get('max_fps')}", (cx, y+gap*2), self.cycle_fps))

        # Quality
        qual = gs.get("quality", "HIGH")
        q_label = self.app.lang.get(f"quality_{qual.lower()}") # e.g. quality_high
        self.buttons.append(Button(f"{self.app.lang.get('gfx_quality')}: {q_label}", (cx, y+gap*3), self.cycle_quality))

        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, y+gap*5), self.init_main_view, ACCENT_RED))

    def _apply_and_save(self):
        # Apply changes immediately
        self.app.apply_graphics_settings(self.app.global_settings)
        # Save to disk
        self.app.data_manager.save_global_settings(self.app.global_settings)
        # Refresh UI
        self.init_graphics_view()

    def cycle_resolution(self):
        idx = self.app.global_settings.get("resolution_idx", 0)
        self.app.global_settings["resolution_idx"] = (idx + 1) % len(RESOLUTIONS)
        self._apply_and_save()

    def toggle_fullscreen(self):
        self.app.global_settings["fullscreen"] = not self.app.global_settings.get("fullscreen")
        self._apply_and_save()

    def cycle_fps(self):
        curr = self.app.global_settings.get("max_fps", 60)
        try:
            nxt = FPS_LIMITS[(FPS_LIMITS.index(curr) + 1) % len(FPS_LIMITS)]
        except:
            nxt = 60
        self.app.global_settings["max_fps"] = nxt
        self._apply_and_save()

    def cycle_quality(self):
        modes = ["LOW", "MED", "HIGH"]
        curr = self.app.global_settings.get("quality", "HIGH")
        try:
            nxt = modes[(modes.index(curr) + 1) % len(modes)]
        except:
            nxt = "HIGH"
        self.app.global_settings["quality"] = nxt
        self._apply_and_save()

    def init_audio_view(self):
        self.current_state = 'AUDIO'
        self.buttons = []
        cx = self._get_center()
        self.buttons.append(Button(f"{self.app.lang.get('audio_sfx')}: TODO", (cx, 250), None))
        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, 400), self.init_main_view, ACCENT_RED))

    def init_language_view(self):
        self.current_state = 'LANGUAGE'
        self.buttons = []
        cx = self._get_center()
        y = 200
        gap = 60
        langs = [("English", "en"), ("Polski", "pl"), ("Deutsch", "de"), ("Español", "es"), ("Français", "fr"), ("Português", "pt")]
        
        for i, (nm, code) in enumerate(langs):
            self.buttons.append(Button(nm, (cx, y + i*gap), lambda c=code: self.change_lang(c)))
        
        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, y + len(langs)*gap + 20), self.init_main_view, ACCENT_RED))

    def change_lang(self, code):
        self.app.lang.load_language(code)
        self.app.global_settings["language"] = code
        self.app.data_manager.save_global_settings(self.app.global_settings)
        self.init_language_view()

    def update(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        t_map = {'MAIN': 'settings_global_title', 'GRAPHICS': 'settings_graphics', 'AUDIO': 'settings_audio', 'LANGUAGE': 'settings_language'}
        title = self.app.lang.get(t_map.get(self.current_state, 'settings_global_title'))
        
        tsurf = self.title_font.render(title, True, TEXT_MAIN)
        trect = tsurf.get_rect(center=(self._get_center(), 100))
        screen.blit(tsurf, trect)
        
        for btn in self.buttons:
            btn.draw(screen)

class PlayerSettingsMenu:
    """
    Handles Player Settings (Nickname Change).
    Accessible ONLY from the In-Game Hub.
    Saves to the specific save slot.
    """
    def __init__(self, app, player, return_callback):
        self.app = app
        self.player = player
        self.return_callback = return_callback
        self.screen = app.screen
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.font_lbl = pg.font.SysFont('Consolas', 28)
        
        self.buttons = []
        self.input_box = None
        self.init_ui()

    def init_ui(self):
        cx = self.app.screen.get_width() // 2
        y = 200
        
        # Input Box
        self.input_box = InputBox((cx, y + 50), self.player.name)
        
        # Save Button
        self.buttons = []
        self.buttons.append(Button(self.app.lang.get("btn_save"), (cx, y + 150), self.save_name, ACCENT_GREEN))
        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, y + 250), self.return_callback, ACCENT_RED))

    def save_name(self):
        new_name = self.input_box.text
        if new_name:
            print(f"[PLAYER] Renaming to {new_name}")
            self.player.set_name(new_name)
            # We don't save to disk immediately here, it saves on exit to menu
        self.return_callback()

    def update(self, event):
        self.input_box.handle_event(event)
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Title
        title = self.app.lang.get("settings_player_title")
        tsurf = self.title_font.render(title, True, TEXT_MAIN)
        trect = tsurf.get_rect(center=(self.app.screen.get_width()//2, 80))
        screen.blit(tsurf, trect)
        
        # Label
        lbl = self.app.lang.get("label_enter_name")
        lsurf = self.font_lbl.render(lbl, True, TEXT_DIM)
        lrect = lsurf.get_rect(center=(self.app.screen.get_width()//2, 180))
        screen.blit(lsurf, lrect)
        
        self.input_box.draw(screen)
        for btn in self.buttons:
            btn.draw(screen)