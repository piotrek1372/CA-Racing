import os
import json
import shutil
from src.constants import DATA_DIR

class DataManager:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.saves_dir = os.path.join(self.data_dir, 'saves')
        self.template_dir = os.path.join(self.saves_dir, 'template')
        self.global_settings_path = os.path.join(self.data_dir, 'settings.json')
        
        # Ensure directories exist
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)

    def check_save_slots(self):
        """Returns dict {1: bool, ...} indicating if save exists."""
        status = {}
        for i in range(1, 4):
            save_path = os.path.join(self.saves_dir, f'save_{i}', 'player_state.json')
            status[i] = os.path.exists(save_path)
        return status

    def create_new_save(self, slot_id):
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

    def save_player_state(self, slot_id, data):
        path = os.path.join(self.saves_dir, f'save_{slot_id}', 'player_state.json')
        return self._save_json(path, data)

    def load_global_settings(self):
        default_settings = {
            "resolution_idx": 0,
            "fullscreen": False,
            "max_fps": 60,
            "quality": "HIGH",
            "language": "en",
            "vol_music": 50, # NEW
            "vol_sfx": 50    # NEW
        }
        
        if not os.path.exists(self.global_settings_path):
            self._save_json(self.global_settings_path, default_settings)
            return default_settings
        
        data = self._load_json(self.global_settings_path)
        for key, val in default_settings.items():
            if key not in data:
                data[key] = val
        return data
        
        if not os.path.exists(self.global_settings_path):
            self._save_json(self.global_settings_path, default_settings)
            return default_settings
        
        data = self._load_json(self.global_settings_path)
        # Merge defaults
        for key, val in default_settings.items():
            if key not in data:
                data[key] = val
        return data

    def save_global_settings(self, data):
        return self._save_json(self.global_settings_path, data)

    def _load_json(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[DATA] Error loading {path}: {e}")
            return {}

    def _save_json(self, path, data):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"[DATA] Error saving {path}: {e}")
            return False