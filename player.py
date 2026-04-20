import pygame

class Player:
    def __init__(self, x, y, speed, image_path):
        try:
            self.img = pygame.image.load(image_path)
            self.img = pygame.transform.scale(self.img, (50, 80))
        except:
            self.img = None
        self.rect = pygame.Rect(x, y, 50, 80)
        self.speed = speed

        # Hitbox réduite pour collisions
        self.hitbox = self.rect.inflate(-10, -10)

    def move(self, keys, left_limit, right_limit, top_limit, bottom_limit):
        if keys[pygame.K_LEFT] and self.rect.left > left_limit:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < right_limit:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > top_limit:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < bottom_limit:
            self.rect.y += self.speed

        # Mettre à jour la hitbox après déplacement
        self.hitbox.topleft = self.rect.topleft

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, self.rect)
        else:
            pygame.draw.rect(screen, (0, 100, 255), self.rect)
