import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien
from pygame.sprite import groupcollide, spritecollideany


def check_keydown_event(event, ai_settings, stats, screen, ship, bullets):
    """Responds to key press"""
    if event.key == pygame.K_RIGHT:
        # move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and len(bullets) < ai_settings.bullet_allowed \
            and stats.game_active:
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


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Watch for keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, stats, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player click the button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset variables to make game playable again
        stats.reset_stats()
        stats.game_active = True

        # Reset score board images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Clear groups
        aliens.remove()
        bullets.remove()

        # reset the game settings to normal
        ai_settings.initilize_dynamic_settings()

        # Build new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        # Center ship
        ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on screen and flip to the new screen"""
    # Redraw the screen after each pass through loop
    screen.fill(ai_settings.bg_color)
    # Draw the score info
    sb.show_score()

    # Draw all the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
        pygame.mouse.set_visible(True)

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """"Updates bullet's position and get rid of old ones"""
    bullets.update()

    # Delete used bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(len(bullets))

    check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


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


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """""Check if the fleet is at an edge, and then update alien's postion"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()

    if stats.ships_left > 0:
        for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
                break
    else:
        stats.game_active = False


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """"Responds to a ship being hit"""

    # Subtract one from ships
    stats.ships_left -= 1
    # Destroy existing aliens
    aliens.empty()
    # Destroy all bullets
    bullets.empty()
    # Create new fleet
    create_fleet(ai_settings, screen, ship, aliens)
    # reposition the ship in the middle of screen
    ship.center_ship()
    # Update scoreboard
    sb.prep_ships()
    # pause for half second
    sleep(0.5)


def check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullets and aliens that have collided"""
    # look for collisions amoung aliens and bullets
    collisions = groupcollide(aliens, bullets, True, False)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)

    if len(aliens) == 0:
        # Start a new level
        stats.level += 1
        sb.prep_level()
        # Destroy bullets
        bullets.empty()
        # Increase game speed
        ai_settings.increase_speed()
        # Create new alien fleet
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """Checks if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
