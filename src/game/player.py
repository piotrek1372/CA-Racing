class Player:
    def __init__(self, player_data, game_db):
        self.name = player_data['player']['name']
        self.money = player_data['player']['money']
        self.level = player_data['player']['level']
        self.exp = player_data['player']['exp']
        self.garage = player_data.get('garage', [])
        self.inventory = player_data.get('inventory', {})
        self.game_db = game_db

    def set_name(self, new_name):
        if new_name: self.name = new_name

    def to_dict(self):
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