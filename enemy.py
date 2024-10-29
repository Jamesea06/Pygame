# enemy.py
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('assets/Commet.png').convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = random.randint(5, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Mett(Enemy):
    def __init__(self):
        super(Mett, self).__init__()
        self.surf = pygame.image.load("assets/Met.png")
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 5  # Default speed
        self.health = 5
        self.transformed = False  # Flag to check if the met has been transformed
        self.hitbox = self.surf.get_bounding_rect()

    # Move the Met based on a constant speed
    # Remove the Met when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def take_damage(self):
        # Reduce health by 1 when hit by a photon
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Destroy boss if health is 0 or below
    
    def transform(self):
        """Change the Mett's image and properties."""
        self.surf = pygame.image.load("assets/Transformed_Met.png").convert_alpha()  # New image
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)  # Optional, if transparency needed
        self.speed = 4  # Increase speed or change other properties
        self.transformed = True  # Mark the met as transformed


class Boss(Enemy):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.image.load("assets/Ship_Boss.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * 4, self.surf.get_height() * 4))
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 250, SCREEN_WIDTH + 300), 300))
        self.speed = 4
        self.target_x = 600
        self.hitbox = self.surf.get_bounding_rect()

    def update(self):
        if self.rect.centerx > self.target_x:
            distance_to_target = self.rect.centerx - self.target_x
            if distance_to_target < 100:
                self.speed = max(1, distance_to_target / 100)
            self.rect.move_ip(-self.speed, 0)
        else:
            self.speed = 0
        self.hitbox.topleft = self.rect.topleft
