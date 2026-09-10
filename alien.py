import pygame, random

# Creating Basic Aliens
class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()

        # Defining Basic Variables of Alien/s
        self.type = type
        path = f"C:/Users/jackie.lu2/OneDrive - NSW Department of Education/Yr9 Game Coding/Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))

    # Alien Movement
    def update(self, direction):
        self.rect.x += direction

# Creating Mystery Ship
class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("C:/Users/jackie.lu2/OneDrive - NSW Department of Education/Yr9 Game Coding/Graphics/mystery.png")

        # Randomly Appearing Mystery Ship: Direction & Randomness
        x = random.choice([self.offset/2, (self.screen_width + self.offset) - self.image.get_width()])
        if x == self.offset/2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft = (x, 90))

    # Mystery Ship Movement (Depending on Direction)
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > (self.screen_width + self.offset/2):
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()