import json
import os
import locale
import sys

class LanguageManager:
    def __init__(self, lang_code=None):
        self.translations = {}
        # Jeśli nie podano kodu, wykryj systemowy
        self.current_lang = lang_code if lang_code else self.detect_system_language()
        self.load_language(self.current_lang)

    def detect_system_language(self):
        """Próbuje wykryć język systemu operacyjnego (zwraca np. 'pl', 'en')."""
        try:
            # Pobierz locale (np. ('pl_PL', 'UTF-8'))
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                # Zwróć tylko pierwsze dwie litery (np. 'pl' z 'pl_PL')
                return sys_lang.split('_')[0].lower()
        except Exception as e:
            print(f"[LANG] Błąd detekcji języka: {e}")
        
        return "en" # Domyślny fallback

    def load_language(self, lang_code):
        """Ładuje plik JSON z folderu data/saves/lang/."""
        self.current_lang = lang_code
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # POPRAWKA ŚCIEŻKI: data/saves/lang zamiast data/lang
        path = os.path.join(base_dir, "data", "lang", f"{lang_code}.json")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            print(f"[LANG] Załadowano język: {lang_code} ze ścieżki: {path}")
        except FileNotFoundError:
            print(f"[LANG] Nie znaleziono pliku: {path}")
            # Jeśli nie znaleziono np. 'pl', spróbuj załadować 'en' jako awaryjny
            if lang_code != "en":
                print("[LANG] Próba załadowania języka awaryjnego (en)...")
                self.load_language("en")
            else:
                self.translations = {}
        except Exception as e:
            print(f"[LANG] Błąd parsowania pliku językowego: {e}")
            self.translations = {}

    def get(self, key):
        """Zwraca tłumaczenie lub klucz, jeśli brakuje tekstu."""
        return self.translations.get(key, f"MISSING:{key}")