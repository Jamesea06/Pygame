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
   #screen.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('Space Race', True, (255, 255, 255))
   start_button = font.render('Space to Start', True, (255, 255, 255))
   screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
   screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
   pygame.display.update()

def draw_game_over_screen():
   #screen.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('Game Over', True, (255, 255, 255))
   restart_button = font.render('R - Restart', True, (255, 255, 255))
   quit_button = font.render('Q - Quit', True, (255, 255, 255))
   screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/3))
   screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
   screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
   pygame.display.update()

def game_over():
    # Display the game over screen and stop the game
    game_state = "Game_over" 
    #pygame.time.wait(2000)   # Pause for 2 seconds before exiting
    player.kill()            # Remove the player
    global running           # Use global to modify the main loop variable
    running = False

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
        self.surf = pygame.image.load("Transformed_Met.png").convert()  # New image
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)  # Optional, if transparency needed
        self.speed = 4  # Increase speed or change other properties
        self.transformed = True  # Mark the met as transformed

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

class Pickable(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Pickable, self).__init__()
        self.surf = pygame.Surface((20, 20))  # Example: a small square
        self.surf.fill((0, 255, 0))  # Example: green color for pickable object
        self.rect = self.surf.get_rect(center=position)  # Position at the location of the destroyed `Mett`
        #self.value = random.randint(10, 50)  # Assign some random value to the pickable object

    def update(self):
        # Add behavior for the pickable object, like floating or spinning if needed
        pass

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.image.load("Ship_Boss.png")
        
        # Resize the image to make it larger (e.g., quadruple the size)
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * 4, self.surf.get_height() * 4))
        
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 250, SCREEN_WIDTH + 300), 300)
        )
        self.speed = 4  # Initial speed
        self.target_x =  600  # Set the target x position (e.g., middle of the screen)

    def update(self):
        # Move the boss leftward
        if self.rect.centerx > self.target_x:
            # Slow down as the boss approaches the target
            distance_to_target = self.rect.centerx - self.target_x
            
            if distance_to_target < 100:  # If close to the target, slow down
                self.speed = max(1, distance_to_target / 100)  # Slow down to a minimum speed of 1
            
            self.rect.move_ip(-self.speed, 0)  # Move left

        else:
            # Stop the boss when it reaches the target
            self.speed = 0


    def transform(self):
        """Change the Mett's image and properties."""
        self.surf = pygame.image.load("Transformed_Met.png").convert()  # New image
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)  # Optional, if transparency needed
        self.speed = 4  # Increase speed or change other properties
        self.transformed = True  # Mark the met as transformed

# Setup for sounds. Defaults are good.
pygame.mixer.init()

pygame.init()

# Load and play background music
pygame.mixer.music.load("370801__romariogrande__space-chase.wav")
pygame.mixer.music.play(loops=-1)

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

# # Create a custom event for adding a new enemy
# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 750)
#ADDMet = pygame.USEREVENT + 2
#pygame.time.set_timer(ADDMet, 5000)
last_enemy_time = 0
last_mett_time = 0
ENEMY_INTERVAL = 1000 
Mett_Interval = 10000
  # Define a variable to track the cooldown time (in milliseconds)
PHOTON_COOLDOWN = 500  # Adjust as needed (500 milliseconds = 0.5 seconds)
last_photon_time = 0  # Variable to store the time when the last photon was created
CollectCount = 0
# Instantiate player. Now
player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
Mette = pygame.sprite.Group()
photon_group = pygame.sprite.Group()
pickable_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
boss_spawned = False
#all_sprites.add(photon) #Generates a photon at

# Run until the user asks to quit
running = True
# Main loop
while running:
    
    # Look at every event in the queue
    for event in pygame.event.get():
        #print(event.type)
        if event.type == QUIT:
                running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                    running = False
            elif event.key == K_SPACE and game_state == "start_menu":
                    game_state = "game"
    # Draw the appropriate screen based on game state
    if game_state == "start_menu":
        draw_start_menu()
    if game_state == "Game_over":
        draw_game_over_screen()
    if game_state == "game":    
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
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_time > ENEMY_INTERVAL and CollectCount != 1:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            last_enemy_time = current_time
        if current_time - last_mett_time > Mett_Interval and CollectCount != 1:
            # Create the new Met and add it to sprite groups
            new_Met = Mett()
            Mette.add(new_Met)
            all_sprites.add(new_Met)
            last_mett_time = current_time

        if CollectCount >0 and not boss_spawned:
            new_Boss = Boss()
            enemies.add(new_Boss)
            all_sprites.add(new_Boss)
            boss_spawned = True
        
        photon_group.update()
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
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, Mette):
            game_over()
        #if pygame.sprite.spritecollideany(photon_group, Mette):
        
        # Check for collisions between photon_group and Mette
        collisions = pygame.sprite.groupcollide(photon_group, Mette, True, False)

        if pygame.sprite.spritecollideany(player, pickable_group):
            print("Collection")
            collection = pygame.sprite.spritecollideany(player, pickable_group)
            CollectCount = CollectCount +1
            collection.kill()
            #for pick in collection.items():
            #    pick.kil()
                

        # Loop through all detected collisions
        if collisions:
            for photon, mets in collisions.items():

                print("Collision detected!")
                for met in mets:  # Loop through each `Mett` in the list
                    if met.transformed:
                               # Create a pickable object at the position of the destroyed `Mett`
                        pickable_object = Pickable(met.rect.center)
                        pickable_group.add(pickable_object)  # Add to a group for pickable items
                        all_sprites.add(pickable_object)  # Add to the all_sprites group for rendering
                        met.kill()
                    else:
                        met.transform()  # Apply the `transform()` method to each `Mett
                        print(met)



        # Draw the player on the screen
        #screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# Done! Time to quit.
pygame.quit()