import pygame, sys, random, time
from player import Player
from background import draw_background
from obstacle import Obstacle
from fuel import Fuel

# --- Initialisation ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

# Joueur
player = Player(WIDTH//2 - 25, HEIGHT-100, 5, "assets/travel.png")

# Obstacles et bonus
obstacle_list = []
fuel_list = []

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

# Charger images obstacles et fuel
obstacle_images = []
for i in range(5):
    path = f"assets/car{i}.png" if i > 0 else "assets/car.png"
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (60, 90))
    obstacle_images.append(img)

fuel_img = pygame.image.load("assets/gasoline.png")
fuel_img = pygame.transform.scale(fuel_img, (40, 40))

gold_img = pygame.image.load("assets/gasoline-pump.png")
gold_img = pygame.transform.scale(gold_img, (40, 40))

# Sons
pygame.mixer.init()
bonus_sound = pygame.mixer.Sound("assets/gamebonus.mp3")
crash_sound = pygame.mixer.Sound("assets/carcrash.mp3")
gold_sound = pygame.mixer.Sound("assets/collect_coins.mp3")

# Score et vies
score = 0
lives = 3
start_time = time.time()
level = 1
last_speed_increase = start_time
obstacle_speed = 5
game_over = False

# Boucle principale
running = True
while running:
    screen.fill((0,0,0))
    draw_background(screen, WIDTH, HEIGHT)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and not game_over:
            # Spawn obstacle
            obstacle_list.append(Obstacle(120, WIDTH-120, obstacle_speed, obstacle_images))
            # Spawn fuel normal ou gold
            if random.randint(1,5) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, gold_img, is_gold=True))
            else:
                if random.randint(1,3) == 1:
                    fuel_list.append(Fuel(120, WIDTH-120, 4, fuel_img))

    if not game_over:
        # Mouvement joueur
        player.move(keys, 120, WIDTH-120, 0, HEIGHT)
        player.draw(screen)

        # Augmentation vitesse tous les 30s
        current_time = time.time()
        if current_time - last_speed_increase >= 30:
            obstacle_speed += 1
            level += 1
            last_speed_increase = current_time

        # Déplacement obstacles
        for obs in obstacle_list[:]:
            obs.update()
            if obs.rect.colliderect(player.hitbox):
                lives -= 1
                if crash_sound: crash_sound.play()
                obstacle_list.remove(obs)
            elif obs.rect.top > HEIGHT:
                obstacle_list.remove(obs)
            else:
                obs.draw(screen)

        # Déplacement fuel
        for f in fuel_list[:]:
            f.update()
            if f.rect.colliderect(player.hitbox):
                if f.is_gold:
                    score += 20
                    if gold_sound: gold_sound.play()
                else:
                    score += 10
                    if bonus_sound: bonus_sound.play()
                fuel_list.remove(f)
            elif f.rect.top > HEIGHT:
                fuel_list.remove(f)
            else:
                f.draw(screen)

        # Texte
        elapsed_time = int(current_time - start_time)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Vies: {lives}", True, (255,255,255)), (10,40))
        screen.blit(font.render(f"Temps: {elapsed_time}s", True, (255,255,255)), (10,70))
        screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (WIDTH-120,10))

        if lives <= 0:
            game_over = True

    else:
        # --- Game Over ---
        screen.blit(big_font.render("GAME OVER", True, (255,50,50)), (WIDTH//2-130, HEIGHT//2-50))
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Rejouer
        replay_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+10, 90, 40)
        quit_rect = pygame.Rect(WIDTH//2+10, HEIGHT//2+10, 90, 40)
        pygame.draw.rect(screen, (0,100,200), replay_rect)
        screen.blit(font.render("Rejouer", True, (255,255,255)), (WIDTH//2-90, HEIGHT//2+18))
        pygame.draw.rect(screen, (200,0,0), quit_rect)
        screen.blit(font.render("Quitter", True, (255,255,255)), (WIDTH//2+20, HEIGHT//2+18))
        if click[0]:
            if replay_rect.collidepoint(mouse_pos):
                # Reset complet
                score = 0
                lives = 3
                level = 1
                obstacle_speed = 5
                obstacle_list.clear()
                fuel_list.clear()
                start_time = time.time()
                last_speed_increase = start_time
                game_over = False
            elif quit_rect.collidepoint(mouse_pos):
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
