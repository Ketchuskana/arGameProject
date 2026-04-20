import pygame
import random

class Obstacle:
    def __init__(self, x_min, x_max, speed, images):
        """
        x_min, x_max : zone horizontale de spawn
        speed : vitesse de descente
        images : liste d'images possibles
        """
        self.img = random.choice(images)
        self.rect = pygame.Rect(
            random.randint(x_min, x_max - self.img.get_width()),
            -self.img.get_height(),
            self.img.get_width(),
            self.img.get_height()
        )
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.img, self.rect)
