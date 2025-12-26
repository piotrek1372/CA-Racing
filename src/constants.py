import os

# --- PATH CONFIGURATION ---
# Points to the root folder of the project (one level up from src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# --- GAME CONSTANTS ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# --- GRAPHICS SETTINGS ---
RESOLUTIONS = [
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080)
]

FPS_LIMITS = [30, 60, 120, 144]

# --- COLORS (R, G, B) ---
BG_COLOR = (30, 30, 30)
PANEL_BG = (50, 50, 55)
TEXT_MAIN = (255, 255, 255)
TEXT_DIM = (150, 150, 150)

ACCENT_GREEN = (50, 200, 50)
ACCENT_RED = (200, 50, 50)
ACCENT_BLUE = (50, 100, 200)
ACCENT_GOLD = (255, 215, 0)

BUTTON_COLOR = (70, 70, 80)
BUTTON_HOVER_COLOR = (100, 100, 120)