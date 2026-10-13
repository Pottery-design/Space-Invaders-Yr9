# Importing Pygame, Random, and All Other Python Files
import os
import pygame, random
from pathlib import Path
from assets import get_asset_path
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

# Level Creator for Formation of Aliens
ALIEN_LEVELS = [
    # Level 1
    [
        [3] * 11,
        [2] * 11,
        [2] * 11,
        [1] * 11,
        [1] * 11,
    ],

    # Level 2
    [
        [0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0],
        [0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 0],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    ],

    # Level 3
    [
        [3] * 4 + [0] * 1 + [3] * 4,
        [3] * 4 + [0] * 1 + [3] * 4,
        [2] * 4 + [0] * 1 + [2] * 4,
        [2] * 4 + [0] * 1 + [2] * 4,
        [1] * 4 + [0] * 1 + [1] * 4,
    ],

    # Level 4
    [
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    ],

    # Level 5
    [
        [3] * 2 + [0] * 1 + [3] * 2 + [0] * 1 + [3] * 2 + [0] * 1 + [3] * 2,
        [2] * 2 + [0] * 1 + [2] * 2 + [0] * 1 + [2] * 2 + [0] * 1 + [2] * 2,
        [1] * 2 + [0] * 1 + [1] * 2 + [0] * 1 + [1] * 2 + [0] * 1 + [1] * 2,
        [0] * 11,
        [1] * 11,
    ],
]

# Game Class: Holds All Game Elements
class Game:
    def __init__(self, screen_width, screen_height, offset):
        # Defining Basic Screen Variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # Defining Spaceship
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))

        # Defining Obstacles
        self.obstacles = self.create_obstacles()

        # Defining Aliens and Mystery Ship
        self.aliens_group = pygame.sprite.Group()
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.level = 1
        self.create_aliens()
        self.aliens_direction = 1

        # Dependent Variables: Lives, Score, Highscore
        self.lives = 3
        self.score = 0
        self.highscore = 0
        self.highscore_file = (
            Path(os.environ.get("LOCALAPPDATA", Path.home()))
            / "SpaceInvaders"
            / "highscore.txt"
        )

        # Defining Constant Variables: Run, Won
        self.won = False
        self.run = True

        # Defining Sound Effects & Music
        self.spaceship_hit = pygame.mixer.Sound(get_asset_path("Sounds/Sounds_spaceship_hit.wav"))
        self.explosion_sound = pygame.mixer.Sound(get_asset_path("Sounds/Sounds_explosion.ogg"))
        self.load_highscore()
        pygame.mixer.music.load(get_asset_path("Sounds/Sounds_music.ogg"))
        pygame.mixer.music.play(-1)

    # Creating Obstacles
    def create_obstacles(self):
        obstacle_width = len(grid[0])*3
        gap = ((self.screen_width + self.offset) - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range (4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    # Creating Aliens
    def create_aliens(self):
        layout = ALIEN_LEVELS[self.level - 1]

        for row, alien_row in enumerate(layout):
            for column, alien_type in enumerate(alien_row):
                if alien_type == 0:
                    continue

                x = 75 + column * 55
                y = 110 + row * 55

                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)

    # Moving Aliens (Left To Right)
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset/2:
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
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    # Detecting Collisions Between Sprites
    def check_for_collisions(self):
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
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
                    self.spaceship_hit.play()
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
        self.won = False
        self.level = 1
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            self.highscore_file.parent.mkdir(parents=True, exist_ok=True)
            with self.highscore_file.open("w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        if not self.highscore_file.exists():
            previous_highscore_file = Path.cwd() / "highscore.txt"
            if previous_highscore_file.is_file():
                self.highscore_file.parent.mkdir(parents=True, exist_ok=True)
                previous_highscore_file.replace(self.highscore_file)

        try:
            with self.highscore_file.open("r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

    def advance_level(self):
        if self.level < len(ALIEN_LEVELS):
            self.level += 1
            self.aliens_direction = 1
            self.alien_lasers_group.empty()
            self.create_aliens()
        else:
            self.won = True
            self.game_over()