import pygame, random

class Fuel:
    def __init__(self, x_min, x_max, speed, image, is_gold=False):
        self.img = image
        self.rect = pygame.Rect(
            random.randint(x_min, x_max - self.img.get_width()),
            -self.img.get_height(),
            self.img.get_width(),
            self.img.get_height()
        )
        self.speed = speed
        self.is_gold = is_gold

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.img, self.rect)
