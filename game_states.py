# game_states.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_start_menu(screen):
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Space Explorer', True, (255, 255, 255))
    start_button = font.render('Space to Start', True, (255, 255, 255))
    controls_title = pygame.font.SysFont('arial', 25).render('Controls:', True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2.5 - title.get_height() / 2))
    screen.blit(start_button, (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT / 2.5 + start_button.get_height() / 2))
    screen.blit(controls_title, ((SCREEN_WIDTH / 2 - controls_title.get_width() / 2, SCREEN_HEIGHT / 1.55 + controls_title.get_height() / 2)))


    Spacebar_image = pygame.image.load('assets/Spacebar.png').convert_alpha()
    Arrow_image = pygame.image.load('assets/Arrow.png').convert_alpha()
    Spacebar_image = pygame.transform.scale(Spacebar_image, (Spacebar_image.get_width() * 2, Spacebar_image.get_height() * 2,))
    Arrow_image = pygame.transform.scale(Arrow_image, (Arrow_image.get_width() * 2, Arrow_image.get_height() * 2,))
    screen.blit(Spacebar_image, (SCREEN_WIDTH / 2.4 - Spacebar_image.get_width() / 2, SCREEN_HEIGHT / 2.2 + Spacebar_image.get_height() / 2))
    screen.blit(Arrow_image, (SCREEN_WIDTH / 1.6 - Arrow_image.get_width() / 2, SCREEN_HEIGHT / 2.1 + Arrow_image.get_height() / 2))



    pygame.display.update()

def draw_game_over_screen(screen):
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (255, 255, 255))
    restart_button = font.render('R - Restart', True, (255, 255, 255))
    quit_button = font.render('Q - Quit', True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 3))
    screen.blit(restart_button, (SCREEN_WIDTH / 2 - restart_button.get_width() / 2, SCREEN_HEIGHT / 1.9 + restart_button.get_height()))
    screen.blit(quit_button, (SCREEN_WIDTH / 2 - quit_button.get_width() / 2, SCREEN_HEIGHT / 2 + quit_button.get_height() / 2))
    pygame.display.update()

def draw_congrats_screen(screen):
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Congratulations!', True, (255, 255, 255))
    message = font.render('You Defeated the Boss!', True, (255, 255, 255))
    restart_button = font.render('Press R to Restart', True, (255, 255, 255))

    # Display the title at the center of the screen
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height()))
    screen.blit(message, (SCREEN_WIDTH / 2 - message.get_width() / 2, SCREEN_HEIGHT / 2))
    screen.blit(restart_button, (SCREEN_WIDTH / 2 - restart_button.get_width() / 2, SCREEN_HEIGHT / 2 + restart_button.get_height() * 2))
    
    pygame.display.update()

def game_over():
    pygame.mixer.music.stop()
    #pygame.time.wait(2000)   # Pause for 2 seconds before exiting
    #player.kill()            # Remove the player