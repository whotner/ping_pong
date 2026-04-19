from pygame import *
from random import *

font.init()
mixer.init()

lost_font = font.SysFont("Arial", 36)
score_font = font.SysFont("Arial", 36)

win_width = 1000
win_height = 700
FPS = 60

player_width = 250
player_heigth = 80
player_speed = 10

ball_size = 70
ball_speed_x = 5
ball_speed_y = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (width, height))

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, speed, up_key, down_key, angle=0):
        super().__init__(player_image, player_x, player_y, width, height, speed)
        self.up_key = up_key
        self.down_key = down_key
        self.image = transform.rotate(self.image, angle)

    def update(self):
        keys = key.get_pressed()

        if keys[self.up_key] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys [self.down_key] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, size, size, 0)
        self.dx = speed_x
        self.dy = speed_y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.dy = -self.dy

    def bounce(self):
        self.dx = -self.dx

    def reset_pos(self):
        self.rect.centerx = win_width // 2
        self.rect.centery = win_height // 2
        self.dx = ball_speed_x if self.dx > 0 else -ball_speed_x
        self.dy = ball_speed_y if randint(0, 1) else -ball_speed_y

window = display.set_mode((win_width, win_height))
display.set_caption('Ping Pong')

background = transform.scale(image.load('midl.png'), (win_width, win_height))

first_player = Player("awp.png", 30, win_height // 2 - player_heigth // 2, player_width, player_heigth, player_speed, K_w, K_s, angle=-90)
second_player = Player("awp2.png", win_width - 100 - player_speed, win_height // 2 - player_heigth // 2, player_width, player_heigth, player_speed, K_UP, K_DOWN, angle=90)
ball = Ball("gaben_ball.png", win_width //2 - ball_size // 2, win_height // 2 - ball_size // 2, ball_size, ball_speed_x, ball_speed_y)

clock = time.Clock()
firstp_score = 0
secondp_score = 0

game = True  
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.blit(background, (0, 0))   

        first_player.update()
        second_player.update()
        ball.update()

        if sprite.collide_rect(ball, first_player) and ball.dx < 0:
            ball.bounce()
            ball.rect.x = first_player.rect.x + first_player.rect.width
        if sprite.collide_rect(ball, second_player) and ball.dx > 0:
            ball.bounce()
            ball.rect.x = second_player.rect.x - ball.rect.width

        if ball.rect.x <= 0:
            secondp_score += 1
            ball.reset_pos()

        if ball.rect.x >= win_width - ball.rect.width:
            firstp_score += 1
            ball.reset_pos()

        left_text = score_font.render(str(firstp_score), True, (255, 255, 255))
        right_text = score_font.render(str(secondp_score), True, (255, 255, 255))
        window.blit(left_text, (win_width // 4, 20))
        window.blit(right_text, (3 * win_width // 4, 20))

        first_player.reset()
        second_player.reset()
        ball.reset()

    clock.tick(FPS) 
    display.update()
