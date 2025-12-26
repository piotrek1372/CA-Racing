import pygame as pg

class Player:
    def __init__(self, player_data, game_db):
        """
        Initializes the Player object using data loaded from JSON.
        :param player_data: Dictionary loaded from player_state.json
        :param game_db: Dictionary loaded from game_data.json (for reference)
        """
        # Base stats
        self.name = player_data['player']['name']
        self.money = player_data['player']['money']
        self.level = player_data['player']['level']
        self.exp = player_data['player']['exp']
        
        # Garage (List of cars owned)
        self.garage = player_data.get('garage', [])
        
        # Inventory (Unmounted parts)
        self.inventory = player_data.get('inventory', {})

        # Reference to the static game database
        self.game_db = game_db

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