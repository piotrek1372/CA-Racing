import pygame as pg
import os
from constants import *

def get_asset_path(filename):
    """Pomocnicza funkcja generująca poprawną ścieżkę do pliku w folderze assets/images."""
    # Pobierz folder, w którym znajduje się ten skrypt (load_assets.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Zbuduj pełną ścieżkę: current_dir/assets/images/filename
    return os.path.join(current_dir, 'assets', 'images', filename)

def load_image(filename, alpha=True):
    """Ładuje obraz z folderu assets/images i konwertuje go dla wydajności."""
    path = get_asset_path(filename)
    
    # Sprawdź czy plik w ogóle istnieje
    if not os.path.exists(path):
        print(f"[ASSETS] BŁĄD: Nie znaleziono pliku: {path}")
        return None

    try:
        img = pg.image.load(path)
        if alpha:
            return img.convert_alpha()  # Dla aut i UI (przezroczystość)
        else:
            return img.convert()        # Dla teł (szybciej)
    except pg.error as e:
        print(f"[ASSETS] Błąd Pygame przy ładowaniu {filename}: {e}")
        return None

def load_game_assets():
    """Główna funkcja ładująca wszystkie zasoby do słownika."""
    assets = {}
    
    print("[ASSETS] Rozpoczynam ładowanie zasobów...")

    # 1. Ładowanie Aut (zakładamy, że masz car-tilemap.png)
    assets['cars'] = load_image('car-tilemap.png', alpha=True)
    
    # 2. Ładowanie Map
    assets['maps'] = []
    # Przykład: map_0.png znajduje się w podfolderze maps
    # Używamy os.path.join, aby połączyć 'maps' i 'map_0.png'
    map_path = os.path.join('maps', 'map_0.png')
    map_img = load_image(map_path, alpha=False)
    
    if map_img:
        assets['maps'].append(map_img)
    
    # Wypisz podsumowanie
    print(f"[ASSETS] Załadowano: {len(assets.keys())} kategorie zasobów.")
    
    return assets