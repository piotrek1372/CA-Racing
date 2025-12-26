import os
import json
import shutil

class Data:
    def __init__(self):
        # Path setup
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.main_dir, 'data')
        self.saves_dir = os.path.join(self.data_dir, 'saves')
        self.template_dir = os.path.join(self.saves_dir, 'template')
        
        # Safety check
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)

    def check_save_slots(self):
        """Returns dict {1: bool, 2: bool, 3: bool} indicating if save exists."""
        status = {}
        for i in range(1, 4):
            save_path = os.path.join(self.saves_dir, f'save_{i}', 'player_state.json')
            status[i] = os.path.exists(save_path)
        return status

    def create_new_save(self, slot_id):
        """Copies template files to save_{slot_id}."""
        target_dir = os.path.join(self.saves_dir, f'save_{slot_id}')
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        src_file = os.path.join(self.template_dir, 'player_state.json')
        dst_file = os.path.join(target_dir, 'player_state.json')
        
        try:
            shutil.copy(src_file, dst_file)
            print(f"[DATA] Created new save in Slot {slot_id}")
            return True
        except Exception as e:
            print(f"[DATA] Error creating save: {e}")
            return False

    def load_game_data(self):
        path = os.path.join(self.template_dir, 'game_data.json')
        return self._load_json(path)

    def load_player_state(self, slot_id):
        path = os.path.join(self.saves_dir, f'save_{slot_id}', 'player_state.json')
        return self._load_json(path)

    # --- TA METODA BYŁA BRAKUJĄCA ---
    def save_player_state(self, slot_id, data):
        """Saves current player state to JSON."""
        path = os.path.join(self.saves_dir, f'save_{slot_id}', 'player_state.json')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[DATA] Game saved to Slot {slot_id}")
            return True
        except Exception as e:
            print(f"[DATA] Error saving game: {e}")
            return False
    # --------------------------------

    def _load_json(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[DATA] Error loading {path}: {e}")
            return {}