# game_states.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_start_menu(screen):
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Space Race', True, (255, 255, 255))
    start_button = font.render('Space to Start', True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 2))
    screen.blit(start_button, (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT / 2 + start_button.get_height() / 2))
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

def game_over():
    pygame.mixer.music.stop()
    #pygame.time.wait(2000)   # Pause for 2 seconds before exiting
    #player.kill()            # Remove the player