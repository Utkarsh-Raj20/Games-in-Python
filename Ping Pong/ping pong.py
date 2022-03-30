import pygame
import random

pygame.init()

WIDTH = 1000
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 40
White = (255, 255, 255)
VEL = 7

light_grey = (200, 200, 200)
running = True
clock = pygame.time.Clock()


# - Player class
class Player:
    def __init__(self, x) -> None:
        self.x = x
        self.y = HEIGHT / 2 - 70
        self.body = pygame.Rect(self.x, self.y, 10, 140)

    def draw(self):
        self.body = pygame.Rect(self.x, self.y, 10, 140)
        pygame.draw.rect(WIN, light_grey, self.body)



# - Scoring variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 28)


# - Speed of the ball
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))

# - Opponent speed
opponent_speed = 5


# - Defining the objects of game
player = Player(10)
opponent = Player(WIDTH - 20)
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)

# - Score timer
score_time = True


def draw_window():
    WIN.fill(pygame.Color("grey12"))
    player.draw()
    opponent.draw()
    pygame.draw.ellipse(WIN, light_grey, ball)
    pygame.draw.aaline(WIN, light_grey, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    player_score_display = game_font.render(f"{player_score}", False, light_grey)
    WIN.blit(player_score_display, (WIDTH / 2 - 16 - 32, HEIGHT / 2 - 16))

    opponent_score_display = game_font.render(f"{opponent_score}", False, light_grey)
    WIN.blit(opponent_score_display, (WIDTH / 2 + 16 + 20, HEIGHT / 2 - 16))

    pygame.display.update()


def handle_player_one(key):
    if key[pygame.K_w] and player.body.y >= 5:
        player.y -= VEL
    if key[pygame.K_s] and player.body.bottom <= HEIGHT - 5:
        player.y += VEL


def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        opponent_score += 1
        reset_all_players()
        score_time = pygame.time.get_ticks()

    if ball.right >= WIDTH:
        player_score += 1
        reset_all_players()
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player.body) and ball_speed_x < 0:
        if abs(ball.left - player.body.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.body.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.body.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent.body) and ball_speed_x > 0:
        if abs(ball.right - opponent.body.left < 10):
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.body.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.body.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def ball_reset():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (WIDTH / 2, HEIGHT / 2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        WIN.blit(number_three, (WIDTH / 2 - 7, HEIGHT / 2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        WIN.blit(number_two, (WIDTH / 2 - 7, HEIGHT / 2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        WIN.blit(number_one, (WIDTH / 2 - 7, HEIGHT / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


def reset_all_players():
    player.y = HEIGHT / 2 - 70
    opponent.y = HEIGHT / 2 - 70


def opponent_movement():
    if ball.top > opponent.body.top and opponent.body.bottom <= HEIGHT - 5:
        opponent.y += opponent_speed
    if ball.top < opponent.body.top and opponent.body.top >= 5:
        opponent.y -= opponent_speed
    if opponent.x <= 0:
        opponent.x = 0


# * MAIN LOOP
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_animation()

    opponent_movement()

    key_pressed = pygame.key.get_pressed()

    handle_player_one(key_pressed)

    draw_window()

    if score_time:
        ball_reset()
    pygame.display.update()

pygame.display.quit()
