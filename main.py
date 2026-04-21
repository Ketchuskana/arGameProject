import os
import sys 
os.environ['OPENCV_VIDEOIO_PRIORITY_BACKEND'] = 'AVFOUNDATION'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import pygame, random, time
import cv2
from player import Player
from background import draw_background
from obstacle import Obstacle
from fuel import Fuel
from boost import BoostManager
from voice_control import VoiceControl
from head_control import HeadControl 

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier - VR Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

boost_manager = BoostManager()
voice = VoiceControl()
head = HeadControl()  

player = Player(WIDTH//2 - 25, HEIGHT-100, 5, "assets/travel.png")

obstacle_list = []
fuel_list = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

obstacle_images = []
for i in range(5):
    path = f"assets/car{i}.png" if i > 0 else "assets/car.png"
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (60, 90))
        obstacle_images.append(img)
    except:
        img = pygame.Surface((60, 90))
        img.fill((200, 0, 0))
        obstacle_images.append(img)

try:
    fuel_img = pygame.image.load("assets/gasoline.png").convert_alpha()
    fuel_img = pygame.transform.scale(fuel_img, (40, 40))
    gold_img = pygame.image.load("assets/gasoline-pump.png").convert_alpha()
    gold_img = pygame.transform.scale(gold_img, (40, 40))
except:
    fuel_img = gold_img = pygame.Surface((40,40))

pygame.mixer.init()
try:
    bonus_sound = pygame.mixer.Sound("assets/gamebonus.mp3")
    crash_sound = pygame.mixer.Sound("assets/carcrash.mp3")
    gold_sound = pygame.mixer.Sound("assets/collect_coins.mp3")
except:
    bonus_sound = crash_sound = gold_sound = None

score = 0
lives = 3
start_time = time.time()
level = 1
last_speed_increase = start_time
obstacle_speed = 5
speed_multiplier = 1
game_over = False

def reset_game():
    global score, lives, level, obstacle_speed, obstacle_list, fuel_list, start_time, last_speed_increase, game_over, speed_multiplier
    score = 0
    lives = 3
    level = 1
    obstacle_speed = 5
    obstacle_list.clear()
    fuel_list.clear()
    start_time = time.time()
    last_speed_increase = start_time
    game_over = False
    speed_multiplier = 1

running = True
while running:
    screen.fill((0,0,0))
    draw_background(screen, WIDTH, HEIGHT)
    keys = pygame.key.get_pressed()
    current_time = time.time()

    head_offset = head.offset
    sensitivity = 45 

    if abs(head_offset) > 0.05:
        player.rect.x += int(head_offset * sensitivity)
    
    if head.debug_frame is not None:
        cv2.imshow("Detection Mouvement", head.debug_frame)
        cv2.waitKey(1)
    
    player.hitbox.topleft = player.rect.topleft

    if player.rect.left < 120: player.rect.left = 120
    if player.rect.right > WIDTH - 120: player.rect.right = WIDTH - 120

    if voice.command:
        if voice.command == "boost":
            boost_manager.activate()
        elif voice.command == "restart" and game_over:
            reset_game()
        elif voice.command == "quit":
            running = False
        elif voice.command == "speed":
            speed_multiplier = 2
        voice.command = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and not game_over:
            obstacle_list.append(Obstacle(120, WIDTH-120, obstacle_speed, obstacle_images))
            if random.randint(1,5) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, gold_img, is_gold=True))
            elif random.randint(1,3) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, fuel_img))

    if not game_over:
        player.move(keys, 120, WIDTH-120, 0, HEIGHT)
        player.draw(screen)

        if current_time - last_speed_increase >= 30:
            obstacle_speed += 1
            level += 1
            last_speed_increase = current_time

        for obs in obstacle_list[:]:
            obs.speed = obstacle_speed * (2 if boost_manager.active else speed_multiplier)
            obs.update()
            if not boost_manager.active and obs.rect.colliderect(player.hitbox):
                lives -= 1
                if crash_sound: crash_sound.play()
                obstacle_list.remove(obs)
            elif obs.rect.top > HEIGHT:
                obstacle_list.remove(obs)
            else:
                obs.draw(screen)

        for f in fuel_list[:]:
            f.update()
            if f.rect.colliderect(player.hitbox):
                score += 20 if f.is_gold else 10
                if f.is_gold and gold_sound: gold_sound.play()
                elif bonus_sound: bonus_sound.play()
                fuel_list.remove(f)
            elif f.rect.top > HEIGHT:
                fuel_list.remove(f)
            else:
                f.draw(screen)

        boost_manager.update()

        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Vies: {lives}", True, (255,255,255)), (10,40))
        screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (WIDTH - 110, 10))
        
        if boost_manager.active:
            screen.blit(font.render("BOOST ACTIF", True, (0,255,0)), (WIDTH//2-60, 10))

        if lives <= 0:
            game_over = True
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        screen.blit(overlay, (0,0))
        
        msg = big_font.render("GAME OVER", True, (255,50,50))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 80))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        replay_rect = pygame.Rect(WIDTH//2 - 130, HEIGHT//2, 120, 50)
        quit_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2, 120, 50)

        color_rep = (0, 150, 255) if replay_rect.collidepoint(mouse_pos) else (0, 100, 200)
        pygame.draw.rect(screen, color_rep, replay_rect, border_radius=8)
        txt_rep = font.render("Rejouer", True, (255,255,255))
        screen.blit(txt_rep, (replay_rect.centerx - txt_rep.get_width()//2, replay_rect.centery - txt_rep.get_height()//2))

        color_quit = (255, 50, 50) if quit_rect.collidepoint(mouse_pos) else (200, 0, 0)
        pygame.draw.rect(screen, color_quit, quit_rect, border_radius=8)
        txt_quit = font.render("Quitter", True, (255,255,255))
        screen.blit(txt_quit, (quit_rect.centerx - txt_quit.get_width()//2, quit_rect.centery - txt_quit.get_height()//2))

        if click[0]:
            if replay_rect.collidepoint(mouse_pos):
                reset_game()
            elif quit_rect.collidepoint(mouse_pos):
                running = False

    pygame.display.flip()
    clock.tick(60)

if hasattr(head, 'stop'): head.stop() 
cv2.destroyAllWindows()
pygame.quit()
sys.exit()