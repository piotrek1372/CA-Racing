import pygame as pg
import os
from constants import *

def get_asset_path(filename):
    """Helper function generating the correct path to a file in the assets/images folder."""
    # Get the folder where this script (load_assets.py) is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build full path: current_dir/assets/images/filename
    return os.path.join(current_dir, 'assets', 'images', filename)

def load_image(filename, alpha=True):
    """Loads an image from assets/images and converts it for performance."""
    path = get_asset_path(filename)
    
    # Check if the file exists at all
    if not os.path.exists(path):
        print(f"[ASSETS] ERROR: File not found: {path}")
        return None

    try:
        img = pg.image.load(path)
        if alpha:
            return img.convert_alpha()  # For cars and UI (transparency)
        else:
            return img.convert()        # For backgrounds (faster)
    except pg.error as e:
        print(f"[ASSETS] Pygame error while loading {filename}: {e}")
        return None

def load_game_assets():
    """Main function loading all resources into a dictionary."""
    assets = {}
    
    print("[ASSETS] Starting resource loading...")

    # 1. Loading Cars (assuming you have car-tilemap.png)
    assets['cars'] = load_image('car-tilemap.png', alpha=True)
    
    # 2. Loading Maps
    assets['maps'] = []
    # Example: map_0.png is located in the maps subfolder
    # Using os.path.join to combine 'maps' and 'map_0.png'
    map_path = os.path.join('maps', 'map_0.png')
    map_img = load_image(map_path, alpha=False)
    
    if map_img:
        assets['maps'].append(map_img)
    
    # Print summary
    print(f"[ASSETS] Loaded: {len(assets.keys())} resource categories.")
    
    return assets