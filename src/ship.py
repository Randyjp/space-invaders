import pygame


class Ship:
    def __init__(self, screen):
        """Initialize the ship and set the starting position"""
        self.screen = screen

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()  # the rectangle of our current screen

        # Star each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx  # match screen's center x
        self.rect.bottom = self.screen_rect.bottom  # match screen's bottom

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update our ship's position based the movements flags"""
        if self.moving_right:
            self.rect.centerx += 1
        elif self.moving_left:
            self.rect.centerx -= 1

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
