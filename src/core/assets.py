import pygame as pg
import os
from src.constants import ASSETS_DIR

def get_asset_path(filename):
    return os.path.join(ASSETS_DIR, 'images', filename)

def load_image(filename, alpha=True):
    path = get_asset_path(filename)
    if not os.path.exists(path):
        print(f"[ASSETS] ERROR: File not found: {path}")
        return None
    try:
        img = pg.image.load(path)
        return img.convert_alpha() if alpha else img.convert()
    except pg.error as e:
        print(f"[ASSETS] Error loading {filename}: {e}")
        return None

def load_game_assets():
    assets = {}
    print("[ASSETS] Loading resources...")
    
    assets['cars'] = load_image('car-tilemap.png', alpha=True)
    
    map_path = os.path.join('maps', 'map_0.png')
    map_img = load_image(map_path, alpha=False)
    
    assets['maps'] = []
    if map_img:
        assets['maps'].append(map_img)
        
    print(f"[ASSETS] Loaded categories: {len(assets)}")
    return assets