import pygame
from laser import Laser

# Defining Spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__ (self, screen_width, screen_height, offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("C:/Users/jackie.lu2/OneDrive - NSW Department of Education/Yr9 Game Coding/Graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.speed = 6

        # Defining Laser Variables
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_sound = pygame.mixer.Sound("Sounds/Sounds_laser.ogg")

    # Registering User Input
    def get_user_input(self):
        keys = pygame.key.get_pressed()

        # Left and Right Movement
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Firing Laser Given Not Recharging
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    # Updating Spaceship & Its Functions
    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    # Prevent Spaceship from Leaving Screen
    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    # Firing Laser Delay
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    # Resetting The Spaceship After GAME_OVER
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.lasers_group.empty()