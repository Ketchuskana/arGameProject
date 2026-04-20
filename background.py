import pygame

def draw_background(screen, width, height):
    # Herbe à gauche et droite
    pygame.draw.rect(screen, (34, 139, 34), (0, 0, 100, height))
    pygame.draw.rect(screen, (34, 139, 34), (width-100, 0, 100, height))
    
    # Route
    pygame.draw.rect(screen, (60, 60, 60), (100, 0, 20, height))           # bord gauche
    pygame.draw.rect(screen, (60, 60, 60), (width-120, 0, 20, height))    # bord droit
    pygame.draw.rect(screen, (100, 100, 100), (120, 0, width-240, height)) # route centrale

    # Lignes blanches continues sur les bords
    pygame.draw.rect(screen, (255, 255, 255), (120, 0, 5, height))
    pygame.draw.rect(screen, (255, 255, 255), (width-125, 0, 5, height))

    # Ligne blanche discontinue au centre
    line_width = 10
    line_height = 30
    gap = 20
    center_x = width // 2
    for y in range(0, height, line_height + gap):
        pygame.draw.rect(screen, (255, 255, 255), (center_x - line_width//2, y, line_width, line_height))
