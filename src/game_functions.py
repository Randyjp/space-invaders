import sys
import pygame

from bullet import Bullet
from alien import Alien
from pygame.sprite import groupcollide

def check_keydown_event(event, ai_settings, screen, ship, bullets):
    """Responds to key press"""
    if event.key == pygame.K_RIGHT:
        # move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and len(bullets) < ai_settings.bullet_allowed:
        # New bullet, goes to the bullet group
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    """Responds to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    """Watch for keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Update images on screen and flip to the new screen"""
    # Redraw the screen after each pass through loop
    screen.fill(ai_settings.bg_color)
    # Draw all the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(aliens, bullets):
    """"Updates bullet's position and get rid of old ones"""
    bullets.update()

    # look for collitions amoung aliens and bullets
    collisions = groupcollide(aliens, bullets, True, True)

    # Delete used bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(len(bullets))


def create_fleet(ai_settings, screen, ship, aliens):
    """"Create the fleet of aliens"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, number_row)


def get_number_aliens_x(ai_settings, alien_width):
    """"Calculate number aliens we can fit on a row"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """"Create an  alien and place it in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """"Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(aliens):
    """Update the position of the aliens in the fleet"""
    aliens.update()


def check_fleet_edges(ai_settings, aliens):
    """Respond if any alien has reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """"Drop the entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    """""Check if the fleet is at an edge, and then update alien's postion"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
