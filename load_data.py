import pygame as pg
import os, json

pg.init()

class Data:
    def __init__(self):
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.main_dir, 'data')

    def load_saves_template(self, file_name):
        fullname = os.path.join(self.data_dir, 'saves', 'template', file_name)
        
        data = None
        try:
            with open(fullname, mode='r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {fullname}")
        except json.JSONDecodeError:
            print(f"Błąd: Plik {file_name} ma niepoprawny format JSON")
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            
        return data