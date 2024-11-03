import pygame
import math

class Pickable(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Pickable, self).__init__()

        # Load multiple images for animation
        self.images = [
            pygame.image.load("assets/colectable1.png").convert_alpha(),
            pygame.image.load("assets/colectable2.png").convert_alpha(),
            pygame.image.load("assets/colectable3.png").convert_alpha(),
            # Add more frames as needed
        ]

        # Scale images
        self.images = [pygame.transform.scale(image, (image.get_width() * 2.5, image.get_height() * 2.5)) for image in self.images]

        self.current_image_index = 0  # Start with the first image
        self.image = self.images[self.current_image_index]  # Initialize the sprite's image
        self.rect = self.image.get_rect(center=position)

        self.animation_speed = 0.1  # Time to wait before changing the frame
        self.animation_time = 0  # Track time for animation

        self.wiggle_amplitude = 1.5  # How much to wiggle (in pixels)
        self.wiggle_speed = 0.15  # Speed of wiggling
        self.wiggle_offset = 1  # Offset to determine current wiggle position

    def update(self):
        # Update the animation frame based on time
        self.animation_time += self.animation_speed
        
        # Change the image every second (or based on a specific time/frames)
        if self.animation_time >= 1:  # Adjust this value for speed
            self.animation_time = 0
            self.current_image_index = (self.current_image_index + 1) % len(self.images)  # Cycle through images
            self.image = self.images[self.current_image_index]  # Update the sprite's image

        # Update the wiggle offset using a sine function
        self.wiggle_offset += self.wiggle_speed
        # Calculate the new y position based on the sine wave
        self.rect.y += math.sin(self.wiggle_offset) * self.wiggle_amplitude

    class FireTrail(pygame.sprite.Sprite):
        def __init__(self, position):
            super(FireTrail, self).__init__()
            # Load multiple images for fire animation
            self.images = [
                pygame.image.load("assets/Fire1.png").convert_alpha(),
                pygame.image.load("assets/Fire2.png").convert_alpha(),
                pygame.image.load("assets/Fire3.png").convert_alpha(),
                # Add more fire frames as needed
            ]

            # Scale images if necessary
            self.images = [pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5)) for image in self.images]

            self.current_image_index = 0  # Start with the first image
            self.image = self.images[self.current_image_index]  # Initialize the sprite's image
            self.rect = self.image.get_rect(center=position)

            self.animation_speed = 0.1  # Time to wait before changing the frame
            self.animation_time = 0  # Track time for animation

        def update(self):
            # Update the animation frame based on time
            self.animation_time += self.animation_speed
            
            # Change the image based on animation time
            if self.animation_time >= 1:  # Adjust this value for speed
                self.animation_time = 0
                self.current_image_index = (self.current_image_index + 1) % len(self.images)  # Cycle through images
                self.image = self.images[self.current_image_index]  # Update the sprite's image