import pygame as pg
import os
from src.constants import ASSETS_DIR

def get_asset_path(category, filename):
    """Helper to construct path to assets subfolders."""
    return os.path.join(ASSETS_DIR, category, filename)

def load_image(filename, alpha=True):
    path = get_asset_path('images', filename)
    if not os.path.exists(path):
        print(f"[ASSETS] ERROR: File not found: {path}")
        return None
    try:
        img = pg.image.load(path)
        return img.convert_alpha() if alpha else img.convert()
    except pg.error as e:
        print(f"[ASSETS] Error loading image {filename}: {e}")
        return None

def load_sound(filename):
    """Loads a sound effect file."""
    path = get_asset_path(os.path.join('sounds', 'sfx'), filename)
    if not os.path.exists(path):
        print(f"[ASSETS] Warning: SFX file not found: {path}")
        return None
    try:
        return pg.mixer.Sound(path)
    except pg.error as e:
        print(f"[ASSETS] Error loading sound {filename}: {e}")
        return None

def load_game_assets():
    """Loads all game resources including images and sounds."""
    assets = {}
    print("[ASSETS] Loading resources...")
    
    # --- IMAGES ---
    assets['cars'] = load_image('car-tilemap.png', alpha=True)
    
    map_path = os.path.join('maps', 'map_0.png')
    map_img = load_image(map_path, alpha=False)
    assets['maps'] = []
    if map_img:
        assets['maps'].append(map_img)
        
    # --- AUDIO (SFX) ---
    # License: JDSherbert (All files included are licensed for commercial & non-commercial projects)
    # Mapping long filenames to short keys for ease of use
    sfx_map = {
        'ui_select': 'JDSherbert - Ultimate UI SFX Pack - Select - 1.ogg',
        'ui_click': 'JDSherbert - Ultimate UI SFX Pack - Select - 2.ogg',
        'ui_cancel': 'JDSherbert - Ultimate UI SFX Pack - Cancel - 1.ogg',
        'ui_back': 'JDSherbert - Ultimate UI SFX Pack - Cancel - 2.ogg',
        'ui_hover': 'JDSherbert - Ultimate UI SFX Pack - Cursor - 1.ogg',
        'ui_error': 'JDSherbert - Ultimate UI SFX Pack - Error - 1.ogg',
        'ui_popup': 'JDSherbert - Ultimate UI SFX Pack - Popup Open - 1.ogg',
        'ui_swipe': 'JDSherbert - Ultimate UI SFX Pack - Swipe - 1.ogg'
    }
    
    assets['sfx'] = {}
    for key, filename in sfx_map.items():
        snd = load_sound(filename)
        if snd:
            assets['sfx'][key] = snd
            
    # --- MUSIC ---
    # We store only paths for music to stream it
    music_dir = os.path.join(ASSETS_DIR, 'sounds', 'music')
    assets['music'] = {
        'main_theme': os.path.join(music_dir, 'Track 1.ogg'),
        'race_theme': os.path.join(music_dir, 'Track 2.ogg'),
        'garage_theme': os.path.join(music_dir, 'Track 3.ogg')
    }

    print(f"[ASSETS] Loaded. SFX count: {len(assets['sfx'])}")
    return assets