class Settings:
    # A class to store all settings for Alien Invasion

    def __init__(self):
        """Initilize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3

        # alien points
        self.alien_points = 50

        # Alien settings
        self.fleet_drop_speed = 10

        # Ship settings
        self.ships_limit = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly points gro
        self.score_scale = 1.5

        self.initilize_dynamic_settings()

    def initilize_dynamic_settings(self):
        """Settings that change during a game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        # 1 = right; -1 = left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increases speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
