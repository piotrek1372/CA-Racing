import pygame as pg
import os
from src.constants import ASSETS_DIR

def get_asset_path(category, filename):
    """Helper to construct path to assets subfolders."""
    return os.path.join(ASSETS_DIR, category, filename)

def load_image(filename, alpha=True):
    """Loads an image from assets/images."""
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
    """Loads a sound effect file from assets/sounds/sfx."""
    path = get_asset_path(os.path.join('sounds', 'sfx'), filename)
    if not os.path.exists(path):
        return None
    try:
        return pg.mixer.Sound(path)
    except pg.error as e:
        print(f"[ASSETS] Error loading sound {filename}: {e}")
        return None

def get_car_sprite(assets, car_id):
    """
    Extracts a specific car sprite from the 6x3 tilemap based on car_id string (e.g., 'car_5').
    Robust: handles car_id being a dict (object) or a string.
    Checks for 'model_id' first, then 'name'.
    """
    if 'cars' not in assets or not assets['cars']:
        return None
    
    if not car_id:
        return None

    # FIX: Handle case where car_id is passed as a full dictionary object
    if isinstance(car_id, dict):
        car_id = car_id.get('model_id') or car_id.get('name', '')
        
    if not isinstance(car_id, str):
        return None

    try:
        # Extract index from ID (e.g., "car_5" -> 5)
        parts = car_id.split('_')
        if len(parts) < 2:
            return None
        index = int(parts[1])
    except (IndexError, ValueError):
        print(f"[ASSETS] Invalid car ID format: {car_id}")
        return None

    sheet = assets['cars']
    sheet_w, sheet_h = sheet.get_size()
    
    # Grid configuration: 6 columns, 3 rows
    cols = 6
    rows = 3
    
    tile_w = sheet_w // cols
    tile_h = sheet_h // rows
    
    # Calculate position
    row = index // cols
    col = index % cols
    
    # Safety check
    if row >= rows:
        print(f"[ASSETS] Car index {index} out of bounds for sprite sheet.")
        return None
        
    rect = pg.Rect(col * tile_w, row * tile_h, tile_w, tile_h)
    return sheet.subsurface(rect)

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
    music_dir = os.path.join(ASSETS_DIR, 'sounds', 'music')
    assets['music'] = {
        'main_theme': os.path.join(music_dir, 'Track 1.ogg'),
        'race_theme': os.path.join(music_dir, 'Track 2.ogg'),
        'garage_theme': os.path.join(music_dir, 'Track 3.ogg')
    }

    print(f"[ASSETS] Loaded. SFX count: {len(assets['sfx'])}")
    return assets