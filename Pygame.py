# Simple pygame program

# Import and initialize the pygame library
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#asurf = pygame.image.load('Ship1.png')

game_state = "start_menu"

def draw_start_menu():
   screen.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('My Game', True, (255, 255, 255))
   start_button = font.render('Start', True, (255, 255, 255))
   screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
   screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
   pygame.display.update()

def draw_game_over_screen():
   screen.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('Game Over', True, (255, 255, 255))
   restart_button = font.render('R - Restart', True, (255, 255, 255))
   quit_button = font.render('Q - Quit', True, (255, 255, 255))
   screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/3))
   screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
   screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
   pygame.display.update()

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load('Ship.png').convert()
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.surf = pygame.image.load('Ship_Up.png').convert()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.surf = pygame.image.load('Ship_Down.png').convert()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.surf = pygame.image.load('Ship.png').convert()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.surf = pygame.image.load('Ship.png').convert()

            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((20, 10))
        self.surf = pygame.image.load('Commet.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,15)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the Met object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Mett(pygame.sprite.Sprite):
    def __init__(self):
        super(Mett, self).__init__()
        self.surf = pygame.image.load("Met.png")
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the Met based on a constant speed
    # Remove the Met when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Photon(pygame.sprite.Sprite):
    def __init__(self, player_position):
        super(Photon, self).__init__()
        self.surf = pygame.Surface((50, 25)) #Size
        self.surf.fill((255, 255, 255)) #Colour
        self.surf = pygame.image.load('Photon.png')
        self.rect = self.surf.get_rect()
        self.velocity = 15  # Set initial velocity
        self.is_moving = False  # Flag to indicate if the photon is moving

        # Set initial position to player's position
        self.rect.center = player_position

    def update(self, *args):
        # Update the position of the photon based on its velocity
        self.rect.move_ip(self.velocity, 0)
        # If the photon moves off-screen, remove it
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Setup for sounds. Defaults are good.
pygame.mixer.init()

pygame.init()

# Load and play background music
#pygame.mixer.music.load("370801__romariogrande__space-chase.wav")
#pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
#move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
#move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
#collision_sound = pygame.mixer.Sound("Collision.ogg")


# Setup the clock for a decent framerate
clock = pygame.time.Clock()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Loading the image
bg_image = pygame.image.load('paul-volkmer-qVotvbsuM_c-unsplash.jpg')
# Image initial position
x = 0

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDMet = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMet, 10000)
  # Define a variable to track the cooldown time (in milliseconds)
PHOTON_COOLDOWN = 500  # Adjust as needed (500 milliseconds = 0.5 seconds)
last_photon_time = 0  # Variable to store the time when the last photon was created

# Instantiate player. Now
player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
Mette = pygame.sprite.Group()
photon_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
#all_sprites.add(photon) #Generates a photon at

# Run until the user asks to quit
running = True
# Main loop
while running:
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
                # Add a new enemy?
    
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
       # Add a new Met?
        elif event.type == ADDMet:
            # Create the new Met and add it to sprite groups
            new_Met = Mett()
            Mette.add(new_Met)
            all_sprites.add(new_Met)
       # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
  


    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
  
        
    if pressed_keys[K_SPACE]:
        current_time = pygame.time.get_ticks()

        if current_time - last_photon_time > PHOTON_COOLDOWN:
            # Create a new instance of the Photon class
            new_photon = Photon(player.rect.center)
            # Add the new photon to sprite groups
            all_sprites.add(new_photon)
            photon_group.add(new_photon)
            # Update the last photon creation time
            last_photon_time = current_time

    photon_group.update()
    # Fill the screen with white
        # Update enemy position
    enemies.update()
    Mette.update()
    screen.fill((0,0,0))
    #screen.blit(bg_image, (0, 0))

    # Moving the background
    x -= 1
    # Resetting the image when it leaves screen
    if x == -1 * bg_image.get_width():
        x = 0
    # Drawing image at position (x,0)
    screen.blit(bg_image, (x, 0))
    #pygame.display.update()
   
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # Draw the player on the screen
    #screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# Done! Time to quit.
pygame.quit()