# photon.py
import pygame
from settings import SCREEN_WIDTH

class Photon(pygame.sprite.Sprite):
    def __init__(self, player_position):
        super(Photon, self).__init__()
        self.surf = pygame.image.load('assets/Photon.png').convert_alpha()
        self.rect = self.surf.get_rect(center=player_position)
        self.velocity = 15

    def update(self):
        self.rect.move_ip(self.velocity, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()
