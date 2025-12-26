import pygame as pg

class Player:
    def __init__(self, player_data, game_db):
        """
        Initializes the Player object using data loaded from JSON.
        Does NOT handle graphics/audio settings anymore.
        """
        # Base stats
        self.name = player_data['player']['name']
        self.money = player_data['player']['money']
        self.level = player_data['player']['level']
        self.exp = player_data['player']['exp']
        
        # Garage & Inventory
        self.garage = player_data.get('garage', [])
        self.inventory = player_data.get('inventory', {})

        # Reference to the static game database
        self.game_db = game_db

    def set_name(self, new_name):
        """Updates the player's nickname."""
        if new_name and len(new_name) > 0:
            self.name = new_name

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
        Note: Settings are NOT included here.
        """
        return {
            "player": {
                "name": self.name,
                "money": self.money,
                "level": self.level,
                "exp": self.exp
            },
            "garage": self.garage,
            "inventory": self.inventory
        }