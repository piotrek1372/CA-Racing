class Player:
    def __init__(self, player_data, game_db):
        self.name = player_data['player']['name']
        self.money = player_data['player']['money']
        self.level = player_data['player']['level']
        self.exp = player_data['player']['exp']
        
        self.garage = player_data.get('garage', [])
        self.inventory = player_data.get('inventory', {})
        
        # Determine current car (load from save or default to first in garage)
        self.current_car = player_data['player'].get('current_car')
        
        # Validation and Fix: Ensure current_car is a String ID, not a Dict object
        if isinstance(self.current_car, dict):
             self.current_car = self.current_car.get('name')

        # Fallback: If no car selected, pick first from garage
        if not self.current_car and self.garage:
            first_car = self.garage[0]
            # Handle if garage contains dict objects
            if isinstance(first_car, dict):
                self.current_car = first_car.get('name')
            else:
                self.current_car = first_car
        
        self.game_db = game_db

    def set_name(self, new_name):
        """Updates player name."""
        if new_name: 
            self.name = new_name

    def set_current_car(self, car_id):
        """
        Sets the active car if the player owns it. 
        Robust check: handles garage being list of strings OR list of dicts.
        """
        found = False
        
        # Iterate to check ownership regardless of data structure
        for item in self.garage:
            if isinstance(item, dict):
                if item.get('name') == car_id:
                    found = True
                    break
            else:
                if item == car_id:
                    found = True
                    break
        
        if found:
            self.current_car = car_id
            return True
        return False

    def to_dict(self):
        """Serializes player state for saving."""
        return {
            "player": {
                "name": self.name,
                "money": self.money,
                "level": self.level,
                "exp": self.exp,
                "current_car": self.current_car  # Save selected car ID
            },
            "garage": self.garage,
            "inventory": self.inventory
        }