import pygame
import random

FPS = 60
CLOCK = pygame.time.Clock()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_BUFFER = 10

BALL_WIDTH = 10
BALL_HEIGHT = 10

AI_PADDLE_SPEED = 2
PLAYER_PADDLE_SPEED = 5
BALL_X_SPEED = 6
BALL_Y_SPEED = 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def draw_ball(x_pos, y_pos):
    ball = pygame.Rect(x_pos, y_pos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)


def draw_paddle_1(y_pos):
    paddle1 = pygame.Rect(PADDLE_BUFFER, y_pos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle1)


def draw_paddle_2(y_pos):
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, y_pos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle2)


def update_ball_pos(game):
    game.ball_x_pos = game.ball_x_pos + game.ball_x_dir * BALL_X_SPEED
    game.ball_y_pos = game.ball_y_pos + game.ball_y_dir * BALL_Y_SPEED

    # if ball hits left paddle
    if (game.ball_x_pos <= PADDLE_BUFFER + PADDLE_WIDTH and game.ball_y_pos + BALL_HEIGHT >= game.paddle_left_y_pos and game.ball_y_pos -
            BALL_HEIGHT <= game.paddle_left_y_pos + PADDLE_HEIGHT):
        game.ball_x_dir = 1
    # if we got scored on
    elif game.ball_x_pos <= 0:
        # potentially reset game here
        scored_on(game)

    # if ball hits right paddle
    if (game.ball_x_pos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER - BALL_WIDTH and game.ball_y_pos + BALL_HEIGHT >=
        game.paddle_right_y_pos and game.ball_y_pos - BALL_HEIGHT <= game.paddle_right_y_pos + PADDLE_HEIGHT):
        game.ball_x_dir = -1
    elif game.ball_x_pos >= WINDOW_WIDTH - BALL_WIDTH:
        scored_on(game)

    if game.ball_y_pos <= 0:
        game.ball_y_pos = 0
        game.ball_y_dir = 1
    elif game.ball_y_pos >= WINDOW_HEIGHT - BALL_HEIGHT:
        game.ball_y_pos = WINDOW_HEIGHT - BALL_HEIGHT
        game.ball_y_dir = -1


def update_ai_paddle_pos(paddle_y_pos, ball_y_pos):
    if ball_y_pos > paddle_y_pos + PADDLE_HEIGHT / 2.0 + 10:
        paddle_y_pos = paddle_y_pos + AI_PADDLE_SPEED
    elif ball_y_pos < paddle_y_pos + PADDLE_HEIGHT / 2.0 - 10:
        paddle_y_pos = paddle_y_pos - AI_PADDLE_SPEED

    if paddle_y_pos < 0:
        paddle_y_pos = 0
    elif paddle_y_pos + PADDLE_HEIGHT > WINDOW_HEIGHT:
        paddle_y_pos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return paddle_y_pos


def update_player_paddle_pos(paddle_y_pos, keys):
    if keys[pygame.K_DOWN]:
        paddle_y_pos = paddle_y_pos + PLAYER_PADDLE_SPEED

    if keys[pygame.K_UP]:
        paddle_y_pos = paddle_y_pos - PLAYER_PADDLE_SPEED

    if paddle_y_pos < 0:
        paddle_y_pos = 0
    elif paddle_y_pos + PADDLE_HEIGHT > WINDOW_HEIGHT:
        paddle_y_pos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return paddle_y_pos


def scored_on(game):
    game.playing = False
    reset_game(game)


def reset_game(game):
    #game.paddle_left_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
    #game.paddle_right_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2

    game.ball_x_dir = 1
    game.ball_y_dir = 1
    game.ball_x_pos = int(WINDOW_WIDTH / 2.0 - BALL_WIDTH / 2.0)
    game.ball_y_pos = int(WINDOW_HEIGHT / 2.0 - BALL_HEIGHT / 2.0)

    num = random.randint(0, 9)
    if(0 < num < 3):
        game.ball_x_dir = 1
        game.ball_y_dir = 1
    if (3 <= num < 5):
        game.ball_x_dir = -1
        game.ball_y_dir = 1
    if (5 <= num < 8):
        game.ball_x_dir = 1
        game.ball_y_dir = -1
    if (8 <= num < 10):
        game.ball_x_dir = -1
        game.ball_y_dir = -1


class Pong:
    def __init__(self):
        self.playing = False

        self.paddle_left_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle_right_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2

        self.ball_x_dir = 1
        self.ball_y_dir = 1
        self.ball_x_pos = int(WINDOW_WIDTH / 2.0 - BALL_WIDTH / 2.0)
        num = random.randint(0, 9)
        self.ball_y_pos = int(num * (WINDOW_HEIGHT - BALL_HEIGHT) / 9.0)

        num = random.randint(0, 9)
        if(0 < num < 3):
            self.ball_x_dir = 1
            self.ball_y_dir = 1
        if (3 <= num < 5):
            self.ball_x_dir = -1
            self.ball_y_dir = 1
        if (5 <= num < 8):
            self.ball_x_dir = 1
            self.ball_y_dir = -1
        if (8 <= num < 10):
            self.ball_x_dir = -1
            self.ball_y_dir = -1

    def get_next_frame(self):
        pygame.event.pump()
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        if not self.playing:
            if keys[pygame.K_SPACE]:
                self.playing = True
            reset_game(self)
        else:
            update_ball_pos(self)

        draw_ball(self.ball_x_pos, self.ball_y_pos)

        # update left paddle
        self.paddle_left_y_pos = update_ai_paddle_pos(self.paddle_left_y_pos, self.ball_y_pos)
        draw_paddle_1(self.paddle_left_y_pos)

        # update right paddle
        self.paddle_right_y_pos = update_player_paddle_pos(self.paddle_right_y_pos, keys)
        draw_paddle_2(self.paddle_right_y_pos)

        pygame.display.flip()


def main():
    game = Pong()
    while True:
        CLOCK.tick(FPS)
        game.get_next_frame()

if __name__ == '__main__':
    main()
