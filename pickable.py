# pickable.py
import pygame

class Pickable(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Pickable, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=position)

    def update(self):
        pass
