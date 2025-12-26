import pygame as pg
from src.constants import *
from src.ui.widgets import Button, InputBox

class GlobalSettingsMenu:
    def __init__(self, app, return_callback):
        self.app = app
        self.return_callback = return_callback
        self.title_font = pg.font.SysFont('Consolas', 50, bold=True)
        self.buttons = []
        self.current_state = 'MAIN'
        self.init_main_view()

    def _get_cx(self):
        return self.app.screen.get_width() // 2

    def init_main_view(self):
        self.current_state = 'MAIN'
        self.buttons = []
        cx = self._get_cx()
        y, gap = 250, 70
        
        opts = [
            (self.app.lang.get("settings_audio"), self.init_audio_view),
            (self.app.lang.get("settings_graphics"), self.init_graphics_view),
            (self.app.lang.get("settings_language"), self.init_language_view),
            (self.app.lang.get("menu_back"), self.return_callback, ACCENT_RED)
        ]
        for i, (txt, act, *c) in enumerate(opts):
            self.buttons.append(Button(txt, (cx, y + i*gap), act, custom_color=c[0] if c else None))

    def init_graphics_view(self):
        self.current_state = 'GRAPHICS'
        self.buttons = []
        cx = self._get_cx()
        y, gap = 150, 70
        gs = self.app.global_settings

        # Res
        res_idx = gs.get("resolution_idx", 0)
        curr_res = RESOLUTIONS[res_idx] if res_idx < len(RESOLUTIONS) else RESOLUTIONS[0]
        self.buttons.append(Button(f"{self.app.lang.get('gfx_resolution')}: {curr_res[0]}x{curr_res[1]}", (cx, y), self.cycle_res))
        # FS
        fs_txt = self.app.lang.get("val_on") if gs.get("fullscreen") else self.app.lang.get("val_off")
        self.buttons.append(Button(f"{self.app.lang.get('gfx_fullscreen')}: {fs_txt}", (cx, y+gap), self.toggle_fs))
        # FPS
        self.buttons.append(Button(f"{self.app.lang.get('gfx_fps')}: {gs.get('max_fps')}", (cx, y+gap*2), self.cycle_fps))
        # Quality
        q = gs.get("quality", "HIGH")
        self.buttons.append(Button(f"{self.app.lang.get('gfx_quality')}: {self.app.lang.get(f'quality_{q.lower()}')}", (cx, y+gap*3), self.cycle_qual))
        
        self.buttons.append(Button(self.app.lang.get("menu_back"), (cx, y+gap*5), self.init_main_view, ACCENT_RED))

    def _save(self):
        self.app.apply_graphics(self.app.global_settings)
        self.app.data_manager.save_global_settings(self.app.global_settings)
        self.init_graphics_view()

    def cycle_res(self):
        self.app.global_settings["resolution_idx"] = (self.app.global_settings.get("resolution_idx", 0) + 1) % len(RESOLUTIONS)
        self._save()
    def toggle_fs(self):
        self.app.global_settings["fullscreen"] = not self.app.global_settings.get("fullscreen")
        self._save()
    def cycle_fps(self):
        curr = self.app.global_settings.get("max_fps", 60)
        self.app.global_settings["max_fps"] = FPS_LIMITS[(FPS_LIMITS.index(curr) + 1) % len(FPS_LIMITS)]
        self._save()
    def cycle_qual(self):
        modes = ["LOW", "MED", "HIGH"]
        self.app.global_settings["quality"] = modes[(modes.index(self.app.global_settings.get("quality","HIGH"))+1)%len(modes)]
        self._save()

    def init_audio_view(self):
        # Placeholder
        self.buttons = [Button(self.app.lang.get("menu_back"), (self._get_cx(), 400), self.init_main_view, ACCENT_RED)]

    def init_language_view(self):
        self.current_state = 'LANGUAGE'
        self.buttons = []
        cx = self._get_cx()
        y, gap = 200, 60
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
        for btn in self.buttons: btn.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        t_map = {'MAIN':'settings_global_title','GRAPHICS':'settings_graphics','AUDIO':'settings_audio','LANGUAGE':'settings_language'}
        t_surf = self.title_font.render(self.app.lang.get(t_map.get(self.current_state)), True, TEXT_MAIN)
        screen.blit(t_surf, t_surf.get_rect(center=(self._get_cx(), 100)))
        for btn in self.buttons: btn.draw(screen)

class PlayerSettingsMenu:
    def __init__(self, app, player, return_cb):
        self.app = app
        self.player = player
        self.return_cb = return_cb
        self.buttons = []
        self.input_box = None
        self.font = pg.font.SysFont('Consolas', 50, bold=True)
        self.init_ui()

    def init_ui(self):
        cx = self.app.screen.get_width() // 2
        self.input_box = InputBox((cx, 250), self.player.name)
        self.buttons = [
            Button(self.app.lang.get("btn_save"), (cx, 350), self.save_name, ACCENT_GREEN),
            Button(self.app.lang.get("menu_back"), (cx, 450), self.return_cb, ACCENT_RED)
        ]

    def save_name(self):
        if self.input_box.text: self.player.set_name(self.input_box.text)
        self.return_cb()

    def update(self, event):
        self.input_box.handle_event(event)
        for b in self.buttons: b.handle_event(event)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        t_surf = self.font.render(self.app.lang.get("settings_player_title"), True, TEXT_MAIN)
        screen.blit(t_surf, t_surf.get_rect(center=(self.app.screen.get_width()//2, 80)))
        
        lbl = pg.font.SysFont('Consolas', 28).render(self.app.lang.get("label_enter_name"), True, TEXT_DIM)
        screen.blit(lbl, lbl.get_rect(center=(self.app.screen.get_width()//2, 180)))
        
        self.input_box.draw(screen)
        for b in self.buttons: b.draw(screen)