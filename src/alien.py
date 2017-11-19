import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """""Initialize the alien and set it on the starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the image and get the alien's rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # start each alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store Alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """"Movie aliens to the right"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        # if self.rect.right >= self.screen_rect.right or self.rect.left <= self.screen_rect.left:
        #     self.ai_settings.fleet_direction *= -1

    def check_edges(self):
        """""change direction of the fleet"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= self.screen_rect.left:
            # self.ai_settings.fleet_direction *= -1
            return True
