import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

# Game Class: Holds All Game Elements
class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True

    # Creating Obstacles
    def create_obstacles(self):
        obstacle_width = len(grid[0])*3
        gap = (self.screen_width - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range (4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    # Creating Aliens
    def create_aliens(self):
        for row in range(5):
            for column in range (11):
                x = 75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x, y)
                self.aliens_group.add(alien)

    # Moving Aliens (Left To Right)
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.aliens_direction = 1
                self.alien_move_down(2)

    # Moving Aliens (Down)
    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    # Aliens Shooting Lasers
    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    # Creating Mystery Ship
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width))

    # Detecting Collisions Between Sprites
    def check_for_collisions(self):
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True):
                    laser_sprite.kill()
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Alien Lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()
    # Beginning And Resetting The Game
    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()