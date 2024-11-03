# enemy.py
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position=None):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('assets/Commet.png').convert_alpha()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        
        if position is None:
            position = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        
        self.rect = self.surf.get_rect(center=position)
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
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH + 1000), 300))
        self.speed = 4
        self.target_x = 600
        self.health = 56 
        self.last_shot_time = 0
        self.shooting_interval = 1000 
         # Create the fire trail
        self.fire_trail = FireTail(self.rect.midright)  # Start at the bottom of the boss

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove boss from the game when health reaches 0
            if hasattr(self, 'fire_trail'):
                self.fire_trail.kill()  # Remove fire trail

    def update(self,player_y):
        if self.rect.centerx > self.target_x:
            distance_to_target = self.rect.centerx - self.target_x
            if distance_to_target < 100:
                self.speed = max(1, distance_to_target / 100)
            self.rect.move_ip(-self.speed, 0)
            self.health = 56 
            fire_trail_width = self.fire_trail.rect.width
            self.fire_trail.rect.center = (self.rect.right + fire_trail_width // 2 -4, self.rect.centery -3)
        else:
            self.speed = 2
            if self.rect.centery < player_y:
                self.rect.move_ip(0, min(self.speed, player_y - self.rect.centery))  # Move down to player's y
            elif self.rect.centery > player_y:
                self.rect.move_ip(0, -min(self.speed, self.rect.centery - player_y))  # Move up to player's y
            fire_trail_width = self.fire_trail.rect.width
            self.fire_trail.rect.center = (self.rect.right + fire_trail_width // 2 -4, self.rect.centery -3)
class FireTail(pygame.sprite.Sprite):
    def __init__(self, position):
        super(FireTail, self).__init__()
        self.images = [
            pygame.image.load("assets/Fire1.png").convert_alpha(),
            pygame.image.load("assets/Fire2.png").convert_alpha(),
            pygame.image.load("assets/Fire3.png").convert_alpha(),
            pygame.image.load("assets/Fire4.png").convert_alpha(),
            pygame.image.load("assets/Fire5.png").convert_alpha(),
        ]
        self.images = [pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3)) for image in self.images]

        self.image = self.images[0]  # Initialize the sprite's image
        self.rect = self.image.get_rect(center=position)

        self.animation_speed = 0.1  # Time to wait before changing the frame
        self.animation_time = 0  # Track time for animation

    def update(self):
        # Update the animation frame based on time
        self.animation_time += self.animation_speed
        
        # Change the image randomly based on animation time
        if self.animation_time >= 1:  # Adjust this value for speed
            self.animation_time = 0
            # Pick a random image from the list
            self.current_image_index = random.randint(0, len(self.images) - 1)  # Randomly select an index
            self.image = self.images[self.current_image_index]  # Update the sprite's image
