import pygame as pg

class Player:
    def __init__(self, player_data, game_db):
        """
        Initializes the Player object using data loaded from JSON.
        """
        # Load core player stats
        self.name = player_data['player']['name']
        self.money = player_data['player']['money']
        self.level = player_data['player']['level']
        self.exp = player_data['player']['exp']
        
        self.garage = player_data.get('garage', [])
        self.inventory = player_data.get('inventory', {})
        self.game_db = game_db

        # --- Graphics & System Settings ---
        # Load settings or apply defaults if missing
        settings_data = player_data.get('settings', {})
        self.settings = {
            "resolution_idx": settings_data.get("resolution_idx", 0), # Default 1280x720
            "fullscreen": settings_data.get("fullscreen", False),
            "max_fps": settings_data.get("max_fps", 60),
            "quality": settings_data.get("quality", "HIGH") # LOW, MED, HIGH
        }

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def to_dict(self):
        """
        Converts the Player object back to a dictionary for JSON saving.
        Includes the settings block.
        """
        return {
            "player": {
                "name": self.name,
                "money": self.money,
                "level": self.level,
                "exp": self.exp
            },
            "garage": self.garage,
            "inventory": self.inventory,
            "settings": self.settings
        }