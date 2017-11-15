import sys
import pygame

from bullet import Bullet


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


def update_screen(ai_settings, screen, ship, bullets):
    """Update images on screen and flip to the new screen"""
    # Redraw the screen after each pass through loop
    screen.fill(ai_settings.bg_color)
    # Draw all the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(bullets):
    """"Updates bullet's position and get rid of old ones"""
    bullets.update()

    # Delete used bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(len(bullets))
