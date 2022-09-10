import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MyGame")

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("project", "space.png")), (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
VEL = 5
FPS = 60
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET_VEL = 15
NUM_BULLETS_MAX = 25
RED_HIT = pygame.USEREVENT + 1
BLACK_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("project", "mixkit-sea-mine-explosion-1184.wav"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("project", "12-Gauge-Pump-Action-Shotgun-Close-Gunshot-A-www.fesliyanstudios.com.mp3"))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BLACK_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("project", "pngfind.com-fighter-jet-png-410089.png"))
BLACK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLACK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("project", "red_spaceship.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(red, black, red_bullets, black_bullets, red_health, black_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    black_health_text = HEALTH_FONT.render("Health: " + str(black_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(black_health_text, (WIDTH - black_health_text.get_width() - 10, 10))
    
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(BLACK_SPACESHIP, (black.x, black.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in black_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)
    
    pygame.display.update()  



def red_controls(keys_pressed, red):
    
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: # left
            red.x -= VEL
    elif keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x: # right
        red.x += VEL
    elif keys_pressed[pygame.K_w] and red.y - VEL > 0: # up
        red.y -= VEL
    elif keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT: # down
        red.y += VEL

def black_controls(keys_pressed, black):
    
    if keys_pressed[pygame.K_LEFT] and black.x - VEL > BORDER.x + 20: # left
        black.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and black.x + VEL > 0: # right
        black.x += VEL
    elif keys_pressed[pygame.K_UP] and black.y - VEL > 0: # up
        black.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and black.y + VEL + black.height < HEIGHT: # down
        black.y += VEL

def handle_bullets(red_bullets, black_bullets, red, black):
    for bullet in black_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            black_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            black_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() / 2, HEIGHT // 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)
        
def main():
    red = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    black = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    black_bullets = []
    red_health = 25
    black_health = 25
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < NUM_BULLETS_MAX:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height // 2 - 10, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(black_bullets) < NUM_BULLETS_MAX:
                    bullet = pygame.Rect(black.x, black.y + black.height // 2 - 10, 10, 5)
                    black_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BLACK_HIT:
                black_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Black wins !!"
        if black_health <= 0:
            winner_text = "Red wins !!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        red_controls(keys_pressed, red)
        black_controls(keys_pressed, black)
        
        handle_bullets(red_bullets, black_bullets, red, black)
        
        draw_window(red, black, red_bullets, black_bullets, red_health, black_health)
          
    main()

if __name__ == "__main__":
    main()