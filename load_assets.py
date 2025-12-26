import pygame as pg
import os
from constants import *

def get_asset_path(filename):
    """Helper function generating the correct path to a file in the assets/images folder."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'assets', 'images', filename)

def load_image(filename, alpha=True):
    """Loads an image from assets/images and converts it for performance."""
    path = get_asset_path(filename)
    
    if not os.path.exists(path):
        print(f"[ASSETS] ERROR: File not found: {path}")
        return None

    try:
        img = pg.image.load(path)
        if alpha:
            return img.convert_alpha()
        else:
            return img.convert()
    except pg.error as e:
        print(f"[ASSETS] Pygame error while loading {filename}: {e}")
        return None

def load_game_assets():
    """Main function loading all resources into a dictionary."""
    assets = {}
    
    print("[ASSETS] Starting resource loading...")

    assets['cars'] = load_image('car-tilemap.png', alpha=True)
    
    # Loading maps from subfolder
    map_path = os.path.join('maps', 'map_0.png')
    map_img = load_image(map_path, alpha=False)
    
    assets['maps'] = []
    if map_img:
        assets['maps'].append(map_img)
    
    print(f"[ASSETS] Loaded: {len(assets.keys())} resource categories.")
    return assets