# player.py
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('assets/Ship.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (50,SCREEN_HEIGHT // 2)
        self.hitbox = self.surf.get_bounding_rect()

    def update(self, pressed_keys=None):
        if pressed_keys is None:
            return
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.surf = pygame.image.load('assets/Ship_Up.png').convert_alpha()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.surf = pygame.image.load('assets/Ship_Down.png').convert_alpha()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.surf = pygame.image.load('assets/Ship.png').convert_alpha()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.surf = pygame.image.load('assets/Ship.png').convert_alpha()

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.hitbox.topleft = self.rect.topleft
