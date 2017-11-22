class GameStats:
    """"Track statistics for alien invasion"""

    def __init__(self, ai_settings):
        """"Initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """"Initiliaze stats that can change during the game"""
        self.ships_left = self.ai_settings.ships_limit
        self.score = 0

