import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")
font = pygame.font.Font(None, 60)
clock = pygame.time.Clock()
MENU = "menu"
PLAYING = "playing"
BOT = 'bot'
PAUSE = 'PAUSE'
PAUSE_BOT = 'PAUSE_BOT'

state = MENU
point_1 = 0
point_2 = 0

bounce_sound = pygame.mixer.Sound("boo.wav")
win_sound = pygame.mixer.Sound("hoo.mp3")

def reset_game():
    global point_1, point_2
    point_1 = 0
    point_2 = 0
    ball.rect.center = (800 // 2, 600 // 2)
    ball.speed_x = random.choice([-5, 5])
    ball.speed_y = random.choice([-5, 5])

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    return text_rect

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 120))
        self.image.fill((255, 255, 255))   
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 11

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < 600:
            self.rect.y += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(800 // 2, 600 // 2))
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.speed_y *= -1

def bot_move(ball, right_paddle):
    if ball.rect.centery < right_paddle.rect.centery and right_paddle.rect.top > 0:
        right_paddle.rect.y -= right_paddle.speed
    elif ball.rect.centery > right_paddle.rect.centery and right_paddle.rect.bottom < 600:
        right_paddle.rect.y += right_paddle.speed

left_paddle = Paddle(50, 600 // 2)
right_paddle = Paddle(800 - 50, 600 // 2)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(left_paddle, right_paddle, ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU:
                if play_button.collidepoint(event.pos):
                    state = PLAYING

                elif play_bot.collidepoint(event.pos):
                    state = BOT
            
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif state == PAUSE:
                if restart.collidepoint(event.pos):
                    reset_game()
                    state = PLAYING

            elif state == PAUSE_BOT:
                if restart.collidepoint(event.pos):
                    reset_game()
                    state = BOT

        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    state = MENU

        elif state == BOT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    state = MENU

    if state == MENU:
       screen.fill((0, 0, 0))
       draw_text("PONG", font, (0, 110, 0), screen, 400, 150)
       play_button = draw_text("Player VS Player", font, (100, 100, 100), screen, 400, 400)
       play_bot = draw_text("Player VS BOT", font, (0, 100, 100), screen, 400, 300)
       quit_button = draw_text("Quit", font, (255, 100, 100), screen, 400, 500)

    elif state == PLAYING:
        screen.fill((0, 0, 0))
        
        left_paddle.move(pygame.K_w, pygame.K_s)
        right_paddle.move(pygame.K_i, pygame.K_j)

        all_sprites.update()

        if pygame.sprite.collide_rect(ball, left_paddle) or pygame.sprite.collide_rect(ball, right_paddle):
            ball.speed_x *= -1.05
            bounce_sound.play()

        if ball.rect.left <= 0:
            point_2 += 1
            ball.rect.center = (800 // 2, 600 // 2)
            ball.speed_x = -7

        elif ball.rect.right >= 800:
            point_1 += 1
            ball.rect.center = (800 // 2, 600 // 2)
            ball.speed_x = -7

        if point_1 == 7 or point_2 == 7:
            win_sound.play()
            state = PAUSE
        
        all_sprites.draw(screen)
        player_1 = draw_text(str(point_1), font, (255, 255, 255), screen, 50, 50)
        player_2 = draw_text(str(point_2), font, (255, 255, 255), screen, 750, 50)
    
    elif state == PAUSE:
        if point_1 == 7:
            draw_text("Player 1 wins!", font, (255, 100, 100), screen, 400, 200)
        else:
            draw_text("Player 2 wins!", font, (255, 100, 100), screen, 400, 200)
        restart = draw_text("RESTART", font, (255, 100, 100), screen, 400, 500)

       
    
    elif state == BOT:
        screen.fill((0, 0, 0))
        
        left_paddle.move(pygame.K_w, pygame.K_s)

        bot_move(ball, right_paddle)

        all_sprites.update()

        if pygame.sprite.collide_rect(ball, left_paddle) or pygame.sprite.collide_rect(ball, right_paddle):
            ball.speed_x *= -1.05
            bounce_sound.play()

        if ball.rect.left <= 0:
            point_2 += 1
            ball.rect.center = (800 // 2, 600 // 2)
            ball.speed_x = -7

        elif ball.rect.right >= 800:
            point_1 += 1
            ball.rect.center = (800 // 2, 600 // 2)
            ball.speed_x = -7

        

        all_sprites.draw(screen)
        player_1 = draw_text(str(point_1), font, (255, 255, 255), screen, 50, 50)
        player_2 = draw_text(str(point_2), font, (255, 255, 255), screen, 750, 50)

        if point_1 == 7 or point_2 == 7:
            win_sound.play()
            state = PAUSE_BOT

    elif state == PAUSE_BOT:
        if point_1 == 7:
            draw_text("Player 1 wins!", font, (255, 100, 100), screen, 400, 200)
        else:
            draw_text("BOT wins!", font, (255, 100, 100), screen, 400, 200)
        restart = draw_text("RESTART", font, (255, 100, 100), screen, 400, 500)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()