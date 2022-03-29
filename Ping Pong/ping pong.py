import pygame
import random

pygame.init()

WIDTH = 1000
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
White = (255, 255, 255)
VEL = 7


player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)


class Player:
    def __init__(self, x) -> None:
        self.x = x
        self.y = HEIGHT / 2 - 70
        self.body = pygame.Rect(self.x, self.y, 10, 140)

    def draw(self):
        self.body = pygame.Rect(self.x, self.y, 10, 140)
        pygame.draw.rect(WIN, (200, 200, 200), self.body)

    def reset_player(self):
        self.body = pygame.Rect(self.x, HEIGHT / 2 - 70, 10, 140)
        pygame.draw.rect(WIN, (200, 200, 200), self.body)


def draw_window(one, two, ball, p_score, o_score):
    WIN.fill(pygame.Color("grey12"))

    one.draw()
    two.draw()
    pygame.draw.ellipse(WIN, (200, 200, 200), ball)
    pygame.draw.aaline(WIN, (200, 200, 200), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    player_score_display = game_font.render(f"{p_score}", False, (200, 200, 200))
    WIN.blit(player_score_display, (WIDTH / 2 - 16 - 32, HEIGHT / 2 - 16))

    opponent_score_display = game_font.render(f"{o_score}", False, (200, 200, 200))
    WIN.blit(opponent_score_display, (WIDTH / 2 + 16 + 20, HEIGHT / 2 - 16))

    pygame.display.update()


def handle_player_one(key, one):
    if key[pygame.K_w] and one.body.y >= 5:
        one.y -= VEL
    if key[pygame.K_s] and one.body.bottom <= HEIGHT - 5:
        one.y += VEL


def main() -> None:
    global player_score, opponent_score

    player_one = Player(10)
    opponent = Player(WIDTH - 20)
    ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)

    ball_speed_x = 6 * random.choice((1, -1))
    ball_speed_y = 6 * random.choice((1, -1))

    opponent_speed = 7

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ~ BALL ANIMATION

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0:
            opponent_score += 1
            # . BALL RESTART
            player_one.y = HEIGHT / 2 - 70
            ball.center = (WIDTH / 2, HEIGHT / 2)
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))

        if ball.right >= WIDTH:
            player_score += 1
            # . BALL RESTART
            ball.center = (WIDTH / 2, HEIGHT / 2)
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))

        if ball.colliderect(player_one.body) or ball.colliderect(opponent.body):
            ball_speed_x *= -1

        # ~ Opponent Movement

        if ball.top > opponent.body.top and opponent.body.bottom <= HEIGHT - 5:
            opponent.y += opponent_speed
        if ball.top < opponent.body.top and opponent.body.top >= 5:
            opponent.y -= opponent_speed
        if opponent.x <= 0:
            opponent.x = 0

        key_pressed = pygame.key.get_pressed()

        handle_player_one(key_pressed, player_one)
        draw_window(player_one, opponent, ball, player_score, opponent_score)
        pygame.display.update()

    pygame.display.quit()


if __name__ == "__main__":
    main()
