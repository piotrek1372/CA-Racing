import pygame as pg
import os
import json
import shutil

class Data:
    def __init__(self):
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.main_dir, 'data')
        self.saves_dir = os.path.join(self.data_dir, 'saves')
        self.template_dir = os.path.join(self.saves_dir, 'template')

    def check_save_slots(self):
        """
        Sprawdza status slotów 1, 2, 3.
        Zwraca słownik, np.: {1: True, 2: False, 3: False} (True = zajęty)
        """
        status = {}
        for i in range(1, 4):
            save_path = os.path.join(self.saves_dir, f'save_{i}', 'player_state.json')
            status[i] = os.path.exists(save_path)
        return status

    def create_new_save(self, slot_id):
        """Tworzy nowy zapis w podanym slocie kopiując szablon."""
        target_dir = os.path.join(self.saves_dir, f'save_{slot_id}')
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        src_file = os.path.join(self.template_dir, 'player_state.json')
        dst_file = os.path.join(target_dir, 'player_state.json')
        
        try:
            shutil.copy(src_file, dst_file)
            print(f"[DATA] Utworzono nowy zapis w Slot {slot_id}")
            return True
        except Exception as e:
            print(f"[DATA] Błąd przy tworzeniu zapisu: {e}")
            return False

    def load_game_data(self):
        """Ładuje statyczną bazę przedmiotów (tylko raz)."""
        path = os.path.join(self.template_dir, 'game_data.json')
        return self._load_json(path)

    def load_player_state(self, slot_id):
        """Ładuje stan gracza z konkretnego slotu."""
        path = os.path.join(self.saves_dir, f'save_{slot_id}', 'player_state.json')
        return self._load_json(path)

    def _load_json(self, path):
        """Pomocnicza funkcja do bezpiecznego ładowania JSON."""
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[DATA] Brak pliku: {path}")
            return None
        except Exception as e:
            print(f"[DATA] Błąd JSON {path}: {e}")
            return None