import json
import os

class LanguageManager:
    def __init__(self, lang_code="en"):
        self.translations = {}
        self.current_lang = lang_code
        self.load_language(lang_code)

    def load_language(self, lang_code):
        """Ładuje plik JSON dla danego kodu języka (np. 'pl', 'en')."""
        self.current_lang = lang_code
        
        # Budowanie ścieżki: data/lang/pl.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "data", "lang", f"{lang_code}.json")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            print(f"[LANG] Załadowano język: {lang_code}")
        except FileNotFoundError:
            print(f"[LANG] Błąd: Nie znaleziono pliku językowego {path}. Używam fallback (pusty).")
            self.translations = {}
        except Exception as e:
            print(f"[LANG] Błąd parsowania języka: {e}")

    def get(self, key):
        """Zwraca przetłumaczony tekst lub sam klucz, jeśli tłumaczenie nie istnieje."""
        return self.translations.get(key, f"MISSING:{key}")

# Opcjonalnie: Prosty sposób na zmianę języka w locie w przyszłości