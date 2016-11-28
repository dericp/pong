import pygame
import random

FPS = 60

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_BUFFER = 10

BALL_WIDTH = 10
BALL_HEIGHT = 10

PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

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

def update_ball_pos(ball_x_pos, ball_y_pos, ball_x_dir, ball_y_dir, paddle_1_y_pos, paddle_2_y_pos):
    ball_x_pos = ball_x_pos + ball_x_dir * BALL_X_SPEED
    ball_y_pos = ball_y_pos + ball_y_dir * BALL_Y_SPEED

    # if ball hits left paddle
    if ball_x_pos <= PADDLE_BUFFER + PADDLE_WIDTH and ball_y_pos + BALL_HEIGHT >= paddle_1_y_pos and ball_y_pos - BALL_HEIGHT <= paddle_1_y_pos + PADDLE_HEIGHT:
        ball_x_dir = 1
    # if we got scored on
    elif ball_x_pos <= 0:
        # potentially reset game here
        ball_x_dir = 1
        return [ball_x_pos, ball_y_pos, ball_x_dir, ball_y_dir, paddle_1_y_pos, paddle_2_y_pos]

    if ball_x_pos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ball_y_pos + BALL_HEIGHT >= paddle_2_y_pos and ball_y_pos - BALL_HEIGHT <= paddle_2_y_pos + PADDLE_HEIGHT:
        ball_x_dir = -1
    elif ball_x_pos >= WINDOW_WIDTH - BALL_WIDTH:
        ball_x_dir = -1
        return [ball_x_pos, ball_y_pos, ball_x_dir, ball_y_dir, paddle_1_y_pos, paddle_2_y_pos]

    if ball_y_pos <= 0:
        ball_y_pos = 0
        ball_y_dir = 1
    elif ball_y_pos >= WINDOW_HEIGHT - BALL_HEIGHT:
        ball_y_pos = WINDOW_HEIGHT - BALL_HEIGHT
        ball_y_dir = -1

    return [ball_x_pos, ball_y_pos, ball_x_dir, ball_y_dir, paddle_1_y_pos, paddle_2_y_pos]

def update_paddle_pos(paddle_y_pos, ball_y_pos):
    if ball_y_pos > paddle_y_pos:
        paddle_y_pos = paddle_y_pos + PADDLE_SPEED
    elif ball_y_pos < paddle_y_pos:
        paddle_y_pos = paddle_y_pos - PADDLE_SPEED

    if paddle_y_pos < 0:
        paddle_y_pos = 0
    elif paddle_y_pos + PADDLE_HEIGHT > WINDOW_HEIGHT:
        paddle_y_pos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return paddle_y_pos

class Pong:
    def __init__(self):
        self.paddle_1_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle_2_y_pos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2

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

        # update vars and draw objects
        [self.ball_x_pos, self.ball_y_pos, self.ball_x_dir, self.ball_y_dir, self.paddle_1_y_pos, self.paddle_2_y_pos] = update_ball_pos(self.ball_x_pos, self.ball_y_pos, self.ball_x_dir, self.ball_y_dir, self.paddle_1_y_pos, self.paddle_2_y_pos)
        draw_ball(self.ball_x_pos, self.ball_y_pos)
        self.paddle_1_y_pos = update_paddle_pos(self.paddle_1_y_pos, self.ball_y_pos)
        draw_paddle_1(self.paddle_1_y_pos)
        self.paddle_2_y_pos = update_paddle_pos(self.paddle_2_y_pos, self.ball_y_pos)
        draw_paddle_2(self.paddle_2_y_pos)

        pygame.display.flip()


def main():
    game = Pong()
    while True:
        game.get_next_frame()

if __name__ == '__main__':
    main()
