# main.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_INTERVAL, Mett_Interval, PHOTON_COOLDOWN
from player import Player
from enemy import Enemy, Mett, Boss
from photon import Photon
from pickable import Pickable
from game_states import draw_start_menu, draw_game_over_screen, game_over
from pygame.locals import RLEACCEL, K_ESCAPE, K_SPACE, KEYDOWN, QUIT, RLEACCEL

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Music and background
pygame.mixer.music.load("sounds/370801__romariogrande__space-chase.wav")
pygame.mixer.music.play(loops=-1)
bg_image = pygame.image.load("assets/paul-volkmer-qVotvbsuM_c-unsplash.jpg")

# Variables.init 
x = 0
last_enemy_time = 0
last_mett_time = 0
last_photon_time = 0 
CollectCount = 0
game_state = "start_menu"
running = True
boss_spawned = False

# Initiate.player

player = Player()
enemies = pygame.sprite.Group()
Mette = pygame.sprite.Group()
photon_group = pygame.sprite.Group()
pickable_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Game.code

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and game_state == "start_menu":
                game_state = "game"
            elif event.key == pygame.K_r and game_state == "Game_over":
                game_state = "game" 
                player = Player()
                # Reset  
                enemies.empty()  
                all_sprites.empty()
                CollectCount = 0
                all_sprites.add(player)
                pygame.mixer.music.load("sounds/370801__romariogrande__space-chase.wav")
                pygame.mixer.music.play(loops=-1)


    screen.fill((0, 0, 0))  # Fill the screen with black before drawing            

    if game_state == "start_menu":
        draw_start_menu(screen)
    elif game_state == "game":
        pressed_keys = pygame.key.get_pressed()
        # Update Player
        player.update(pressed_keys)
        if pressed_keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_photon_time > PHOTON_COOLDOWN:
                new_photon = Photon(player.rect.center)
                all_sprites.add(new_photon)
                photon_group.add(new_photon)
                last_photon_time = current_time     
        current_time = pygame.time.get_ticks()
        # New photon
        if current_time - last_enemy_time > ENEMY_INTERVAL and CollectCount != 1:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            last_enemy_time = current_time
        # New Meteorite
        if current_time - last_mett_time > Mett_Interval and CollectCount != 1:
            new_Met = Mett()
            Mette.add(new_Met)
            all_sprites.add(new_Met)
            last_mett_time = current_time
        # New Boss
        if CollectCount >0 and not boss_spawned:
            new_Boss = Boss()
            enemies.add(new_Boss)
            all_sprites.add(new_Boss)
            boss_spawned = True
        # Update sprites
        photon_group.update()
        enemies.update()
        Mette.update()
        # Background
        x -= 1  # Move the background leftward
        if x <= -bg_image.get_width():
            x = 0
        screen.blit(bg_image, (x, 0))
        screen.blit(bg_image, (x + bg_image.get_width(), 0))  # Draw second instance for seamless effect

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Collisoin Detection
        # Player
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, Mette):
            game_state = "Game_over"
            game_over()
            player.kill()
               
       # Collectable
        if pygame.sprite.spritecollideany(player, pickable_group):
            collection = pygame.sprite.spritecollideany(player, pickable_group)
            CollectCount = CollectCount +1
            collection.kill()
                
        # Meteorite
        collisions = pygame.sprite.groupcollide(photon_group, Mette, True, False)
        if collisions:
            for photon, mets in collisions.items():
                for met in mets:
                    if met.transformed:
                        pickable_object = Pickable(met.rect.center)
                        pickable_group.add(pickable_object)
                        all_sprites.add(pickable_object)
                        met.kill()
                    else:
                        met.transform()
        # Draw updated Sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
    
    # Game over
    elif game_state == "Game_over":
        draw_game_over_screen(screen) 

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
