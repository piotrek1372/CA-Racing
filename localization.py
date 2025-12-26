import json
import os
import locale
import sys

class LanguageManager:
    def __init__(self, lang_code=None):
        self.translations = {}
        # If no code is provided, detect the system language
        self.current_lang = lang_code if lang_code else self.detect_system_language()
        self.load_language(self.current_lang)

    def detect_system_language(self):
        """Attempts to detect the operating system language (returns e.g., 'pl', 'en')."""
        try:
            # Get locale (e.g., ('pl_PL', 'UTF-8'))
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                # Return only the first two letters (e.g., 'pl' from 'pl_PL')
                return sys_lang.split('_')[0].lower()
        except Exception as e:
            print(f"[LANG] Language detection error: {e}")
        
        return "en" # Default fallback

    def load_language(self, lang_code):
        """Loads the JSON file from the data/saves/lang/ folder."""
        self.current_lang = lang_code
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Path correction: data/saves/lang instead of data/lang
        path = os.path.join(base_dir, "data", "saves", "lang", f"{lang_code}.json")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            print(f"[LANG] Loaded language: {lang_code} from path: {path}")
        except FileNotFoundError:
            print(f"[LANG] File not found: {path}")
            # If e.g., 'pl' is not found, try to load 'en' as backup
            if lang_code != "en":
                print("[LANG] Attempting to load backup language (en)...")
                self.load_language("en")
            else:
                self.translations = {}
        except Exception as e:
            print(f"[LANG] Language file parsing error: {e}")
            self.translations = {}

    def get(self, key):
        """Returns the translation or the key itself if the text is missing."""
        return self.translations.get(key, f"MISSING:{key}")