import pygame


class Ship:
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set the starting position"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()  # this is the ship's rect
        self.screen_rect = screen.get_rect()  # the rect of our current screen

        # Star each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx  # match screen's center x
        self.rect.bottom = self.screen_rect.bottom  # match screen's bottom

        # store a decimal value for the ships' center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update our ship's position based the movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect object from self center(just the int part)
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """"Centers the ship"""
        self.center = self.screen_rect.centerx