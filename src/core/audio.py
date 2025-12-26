import pygame as pg

class AudioManager:
    """
    Handles music streaming and SFX playback.
    Integrates with global settings for volume control.
    Credits: SFX by JDSherbert.
    """
    def __init__(self, app):
        self.app = app
        self.assets = app.assets
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Load initial volume from settings
        self.load_volume_settings()
        
        # Current track tracking
        self.current_music = None

    def load_volume_settings(self):
        """Updates internal volume variables from global settings."""
        settings = self.app.global_settings
        self.music_volume = settings.get("vol_music", 50) / 100.0
        self.sfx_volume = settings.get("vol_sfx", 50) / 100.0
        
        # Apply immediately
        pg.mixer.music.set_volume(self.music_volume)
        
    def play_music(self, track_key):
        """Streams music from disk."""
        path = self.assets['music'].get(track_key)
        if not path:
            print(f"[AUDIO] Music track not found: {track_key}")
            return

        if self.current_music == track_key and pg.mixer.music.get_busy():
            return # Already playing this track

        try:
            pg.mixer.music.load(path)
            pg.mixer.music.play(-1) # Loop indefinitely
            pg.mixer.music.set_volume(self.music_volume)
            self.current_music = track_key
            print(f"[AUDIO] Playing music: {track_key}")
        except Exception as e:
            print(f"[AUDIO] Error playing music: {e}")

    def play_sfx(self, sfx_key):
        """Plays a sound effect if loaded."""
        sound = self.assets['sfx'].get(sfx_key)
        if sound:
            sound.set_volume(self.sfx_volume)
            sound.play()
        else:
            # Silent fail or debug print
            pass

    def set_music_volume(self, percent):
        """Sets music volume (0-100) and saves to settings."""
        self.app.global_settings["vol_music"] = percent
        self.music_volume = percent / 100.0
        pg.mixer.music.set_volume(self.music_volume)
        self.app.data_manager.save_global_settings(self.app.global_settings)

    def set_sfx_volume(self, percent):
        """Sets SFX volume (0-100) and saves to settings."""
        self.app.global_settings["vol_sfx"] = percent
        self.sfx_volume = percent / 100.0
        self.app.data_manager.save_global_settings(self.app.global_settings)