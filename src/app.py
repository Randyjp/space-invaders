import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make our ship
    ship = Ship(ai_settings, screen)
    # Make a sprite group to store bullets
    bullets = Group()
    # Store the alien fleet
    aliens = Group()
    # Create and instance to store in game stats
    stats = GameStats(ai_settings)

    # Create the fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create play button
    play_button = Button(ai_settings, screen, "Play")

    # create a score board
    sb = Scoreboard(ai_settings, screen, stats)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
