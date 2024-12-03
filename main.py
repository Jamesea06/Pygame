# main.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_INTERVAL, Mett_Interval, PHOTON_COOLDOWN
from player import Player
from enemy import Enemy, Mett, Boss, FireTail, Explosion
from photon import Photon
from pickable import Pickable
from game_states import draw_start_menu, draw_game_over_screen, draw_congrats_screen
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
congrats_delay = 3000  # 2 seconds delay
boss_defeated_time = None  # To store the time when the boss is defeated
boss_fire_pos = 500  # Change this to the y-position you want
fire_delay = 2000  # 2-second delay in milliseconds
fire_pause = 5000
boss_fire_time = None
boss_fire_pause = None
boss_music_played = False
music_transition_start = None
transitioning_music = False
fade_duration = 2500  # Duration of fade in milliseconds

# Initiate.player

player = Player()
enemies = pygame.sprite.Group()
Mette = pygame.sprite.Group()
boss = pygame.sprite.Group()
Fire = pygame.sprite.Group()
photon_group = pygame.sprite.Group()
pickable_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
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
            elif event.key == pygame.K_r and (game_state == "Game_over" or game_state == "congrats"):
                game_state = "game" 
                player = Player()
                enemies.empty()
                boss.empty()
                Mette.empty()
                photon_group.empty()    
                pickable_group.empty()
                Fire.empty()
                all_sprites.empty()
                CollectCount = 0
                boss_fire_time = None
                boss_fire_pause = None
                boss_spawned = False
                boss_music_played = False
                transitioning_music = False
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
        # New Photon
        if pressed_keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_photon_time > PHOTON_COOLDOWN:
                new_photon = Photon(player.rect.center)
                all_sprites.add(new_photon)
                photon_group.add(new_photon)
                last_photon_time = current_time     
        current_time = pygame.time.get_ticks()
        # New Enemy
        if current_time - last_enemy_time > ENEMY_INTERVAL and CollectCount != 3:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            last_enemy_time = current_time
        
        if boss_spawned:
            for boss_sprite in boss:
                if boss_sprite.rect.x <= boss_fire_pos:
                    if boss_fire_time is None:
                        boss_fire_time = pygame.time.get_ticks() 
                    if pygame.time.get_ticks() - boss_fire_time >= fire_delay:     
                        new_enemy = Enemy(boss_sprite.rect.midleft)
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)
                        if boss_fire_pause == None:
                            boss_fire_pause = pygame.time.get_ticks() 
                        if pygame.time.get_ticks() - boss_fire_pause >= fire_pause:
                            boss_fire_pause = None
                            boss_fire_time = None
                    
        # New Meteorite
        if current_time - last_mett_time > Mett_Interval and CollectCount != 3:
            new_Met = Mett()
            Mette.add(new_Met)
            all_sprites.add(new_Met)
            last_mett_time = current_time
        # New Boss
        if CollectCount >2 and not boss_spawned:
            new_Boss = Boss()
            boss.add(new_Boss)
            Fire.add(new_Boss.fire_trail)
            all_sprites.add(new_Boss)
            boss_spawned = True
        
        if boss_spawned and not boss_music_played and not transitioning_music:
            # Start fading out the music, set transition start time
            pygame.mixer.music.fadeout(fade_duration)
            music_transition_start = pygame.time.get_ticks()
            transitioning_music = True  # Begin transition process
        if transitioning_music:
            if pygame.time.get_ticks() - music_transition_start >= fade_duration:
                pygame.mixer.music.load("sounds/683457__seth_makes_sounds__dope-video-game-boss-music.wav")
                pygame.mixer.music.play(loops=-1, fade_ms=fade_duration, start=4)  # Start with a fade-in
                boss_music_played = True
                transitioning_music = False  # Transition complete

        # Update sprites
        photon_group.update()
        enemies.update()
        boss.update(player.rect.centery)
        pickable_group.update()
        Mette.update()
        Fire.update()
        explosions_group.update()
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
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, Mette) or pygame.sprite.spritecollideany(player, boss):
            game_state = "Game_over"
            pygame.mixer.music.stop()
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
                        #all_sprites.add(pickable_object)
                        met.kill()
                    else:
                        met.transform()
        # Boss
        collide = pygame.sprite.groupcollide(photon_group, boss, True, False)
        if collide:
            for photon, bosses in collide.items():
                for collided_boss in bosses:
                    collided_boss.take_damage()
                    if collided_boss.health <= 0 and boss_defeated_time is None:
                        explosions_group.add(new_Boss.explosion)
                        boss_defeated_time = pygame.time.get_ticks()  # Record the current time
        
        current_time = pygame.time.get_ticks()
        if boss_defeated_time is not None and current_time - boss_defeated_time >= congrats_delay:
            game_state = "congrats"
            boss_defeated_time = None  # Reset after switching game state
                        
        # Draw updated Sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for drawn in pickable_group:   
            screen.blit(drawn.image, drawn.rect)
        for Flame in Fire:   
            screen.blit(Flame.image, Flame.rect)
        for explosion in explosions_group:
            screen.blit(explosion.image, explosion.rect)
    
    # Game over
    elif game_state == "Game_over":
        draw_game_over_screen(screen) 

    elif game_state == "congrats":
        draw_congrats_screen(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
