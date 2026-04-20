import pygame, sys, random, time
from player import Player
from background import draw_background
from obstacle import Obstacle
from fuel import Fuel
from boost import BoostManager
from voice_control import VoiceControl

# --- Initialisation ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

# Managers
boost_manager = BoostManager()
voice = VoiceControl()

frame_count = 0

# Joueur
player = Player(WIDTH//2 - 25, HEIGHT-100, 5, "assets/travel.png")

# Obstacles et bonus
obstacle_list = []
fuel_list = []

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

# Images
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
base_speed = 5
game_over = False

def reset_game():
    global score, lives, level, base_speed, obstacle_list, fuel_list, start_time, last_speed_increase, game_over
    score = 0
    lives = 3
    level = 1
    base_speed = 5
    obstacle_list.clear()
    fuel_list.clear()
    start_time = time.time()
    last_speed_increase = start_time
    game_over = False

# Boucle principale
running = True
while running:
    frame_count += 1
    screen.fill((0,0,0))
    draw_background(screen, WIDTH, HEIGHT)

    keys = pygame.key.get_pressed()

    # --- VOIX (toutes les ~2 sec) ---
    if frame_count % 120 == 0:
        voice.listen()

    if voice.command:
        if "boost" in voice.command:
            boost_manager.activate()

        if "restart" in voice.command and game_over:
            reset_game()

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == SPAWN_EVENT and not game_over:
            current_speed = base_speed * 2 if boost_manager.active else base_speed

            obstacle_list.append(Obstacle(120, WIDTH-120, current_speed, obstacle_images))

            if random.randint(1,5) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, gold_img, is_gold=True))
            else:
                if random.randint(1,3) == 1:
                    fuel_list.append(Fuel(120, WIDTH-120, 4, fuel_img))

    # --- UPDATE BOOST ---
    boost_manager.update()

    if not game_over:

        # Mouvement joueur
        player.move(keys, 120, WIDTH-120, 0, HEIGHT)
        player.draw(screen)

        current_time = time.time()

        # Level up
        if current_time - last_speed_increase >= 30:
            base_speed += 1
            level += 1
            last_speed_increase = current_time

        current_speed = base_speed * 2 if boost_manager.active else base_speed

        # Obstacles
        for obs in obstacle_list[:]:
            obs.speed = current_speed
            obs.update()

            # ❗ collision désactivée si boost actif
            if not boost_manager.active and obs.rect.colliderect(player.hitbox):
                lives -= 1
                if crash_sound: crash_sound.play()
                obstacle_list.remove(obs)

            elif obs.rect.top > HEIGHT:
                obstacle_list.remove(obs)
            else:
                obs.draw(screen)

        # Fuel
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

        # UI
        elapsed_time = int(current_time - start_time)

        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Vies: {lives}", True, (255,255,255)), (10,40))
        screen.blit(font.render(f"Temps: {elapsed_time}s", True, (255,255,255)), (10,70))
        screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (WIDTH-120,10))

        # 🔥 BOOST UI
        screen.blit(font.render(f"Boosts: {boost_manager.available_boosts}", True, (255,255,255)), (10,100))

        if boost_manager.active:
            screen.blit(font.render("BOOST ACTIVÉ", True, (0,255,0)), (10,130))

        if lives <= 0:
            game_over = True

    else:
        # --- GAME OVER ---
        screen.blit(big_font.render("GAME OVER", True, (255,50,50)), (WIDTH//2-130, HEIGHT//2-50))

        screen.blit(font.render("Dire 'RESTART' pour rejouer", True, (255,255,255)), (WIDTH//2-150, HEIGHT//2+60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()