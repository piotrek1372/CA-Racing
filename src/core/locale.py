import json
import os
import locale
from src.constants import DATA_DIR

class LanguageManager:
    def __init__(self, lang_code=None):
        self.translations = {}
        self.current_lang = lang_code if lang_code else self.detect_system_language()
        self.load_language(self.current_lang)

    def detect_system_language(self):
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                return sys_lang.split('_')[0].lower()
        except Exception as e:
            print(f"[LANG] Language detection error: {e}")
        return "en"

    def load_language(self, lang_code):
        self.current_lang = lang_code
        # Path fixed to point to data/lang
        path = os.path.join(DATA_DIR, "lang", f"{lang_code}.json")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            print(f"[LANG] Loaded language: {lang_code}")
        except FileNotFoundError:
            print(f"[LANG] File not found: {path}")
            if lang_code != "en":
                self.load_language("en")
            else:
                self.translations = {}
        except Exception as e:
            print(f"[LANG] Error: {e}")
            self.translations = {}

    def get(self, key):
        return self.translations.get(key, f"MISSING:{key}")