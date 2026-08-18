import pygame, random

# Creating Basic Aliens
class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"C:/Users/jackie.lu2/OneDrive - NSW Department of Education/Yr9 Game Coding/Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        self.rect.x += direction

# Creating Mystery Ship
class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.image = pygame.image.load("C:/Users/jackie.lu2/OneDrive - NSW Department of Education/Yr9 Game Coding/Graphics/mystery.png")
        self.screen_width = screen_width

        x = random.choice([0, self.screen_width - self.image.get_width()])
        if x == 0:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft = (x, 40))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width:
            self.kill()
        elif self.rect.left < 0:
            self.kill()