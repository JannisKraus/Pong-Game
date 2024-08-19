import random

import pygame

from Paddle import Paddle
from Ball import Ball
from Settings import *
import time
from Powerups import Powerups

pygame.init()


class Game:

    def __init__(self, window):
        self.window = window
        self.left_paddle = Paddle(window, 10,WIN_HEIGHT/2-PADDLE_HEIGHT/2,WHITE)
        self.right_paddle = Paddle(window, WIN_WIDTH -30, WIN_HEIGHT/2-PADDLE_HEIGHT/2, WHITE )
        self.ball = Ball(window,WIN_WIDTH/2,WIN_HEIGHT/2,BLUE)
        self.left_score = 0
        self.right_score = 0

        self.left_hits = 0

        if POWERUPS_ENABLED:
            self.powerups = Powerups()
            self.powerup_active = False
            self.powerup_visable = False
            self.last_powerup_time = millis()

    def draw(self):
        # This is our central draw method. If we want to display something on the screen, we have to add it in here.
        

        # Define the background.
        if BG_IMG is None:
            # Fill the background with a specified color.
            self.window.fill(BLACK)
        else:
            # Fill the background with an image you can specify in the Settings.py file.
            self.window.blit(BG_IMG, (0, 0))

        # Draw the dividing lines in the middle
        self.draw_divider()

        if POWERUPS_ENABLED and self.powerup_visable:
            if millis() - self.last_powerup_time > POWERUP_DISPLAY_TIME:
                self.hide_powerup()
            else:
                self.powerups.draw(self.window)



        # TODO Paddle (1) Draw the paddles
        self.left_paddle.draw()
        self.right_paddle.draw()
        # TODO Ball (3) Draw the ball
        self.ball.draw()
        # TODO Score (7) Draw the score
        self.draw_score()
        # We have to call this one to make sure our drawings get displayed.
        pygame.display.update()

    def draw_divider(self):
        # Draws the dividing lines in the middle of the screen.
        for i in range(10, WIN_HEIGHT, WIN_HEIGHT // 5):
            pygame.draw.rect(self.window, WHITE, (WIN_WIDTH // 2 - 2.5 , i, 5, WIN_HEIGHT // 15))

    def draw_text(self, text, x, y, color=RED) -> None:
        text = FONT.render(text, True, color)
        x = x - text.get_width() // 2
        self.window.blit(text, (x, y))

    # TODO Paddle (2) Move the paddles
    #   They should respond to key presses.
    def move_paddle_keys(self, keys):
        # TODO: define "up" and "down" keys for left and right paddle
        left_paddle_up_key = pygame.K_w
        left_paddle_down_key = pygame.K_s
        right_paddle_up_key = pygame.K_UP
        right_paddle_down_key = pygame.K_DOWN

        # Move left paddle upwards with w and downwards with s
        if keys[left_paddle_up_key]:
            upwards = True  # TODO: True or False?
            self.left_paddle.move(upwards)
        if keys[left_paddle_down_key]:
            upwards = False  # TODO: True or False?
            self.left_paddle.move(upwards)

        # Move right paddle upwards with up arrow and downwards with down arrow
        if keys[right_paddle_up_key]:
            upwards = True  # TODO: True or False?
            self.right_paddle.move(upwards)
        if keys[right_paddle_down_key]:
            upwards = False  # TODO: True or False?
            self.right_paddle.move(upwards)

    # region TODO (6) Collision detection
    # TODO Ball (6) Collision detection
    def handle_collision(self):
        if (POWERUPS_ENABLED and self.powerup_visable and self.ball_hits_powerup()):
            self.handle_powerup_collision()


        if self.ball_hits_ceiling_or_floor():
            # TODO: Reverse y direction if we hit the ceiling or bottom of the screen.
            self.ball.y_vel *= (-1 * random.uniform(0.8, 1.2))
            pass

        if self.ball_hits_paddle(self.left_paddle):
            # TODO: handle collision with left paddle
            self.handle_paddle_collision(self.left_paddle)
            self.left_hits += 1
            pass
        elif self.ball_hits_paddle(self.right_paddle):
            # TODO: handle collision with right paddle
            self.handle_paddle_collision(self.right_paddle)
            pass

    def ball_hits_ceiling_or_floor(self):
        return self.ball.y + BALL_RADIUS > WIN_HEIGHT or self.ball.y - BALL_RADIUS < 0
        # TODO: condition must be True when ball hits the ceiling or bottom, False otherwise

    def ball_hits_powerup(self):
        return ((self.powerups.x - BALL_RADIUS <= self.ball.x <= self.powerups.x + POWERUP_SIZE + BALL_RADIUS) and
                (self.powerups.y - BALL_RADIUS <= self.ball.y <= self.powerups.y + POWERUP_SIZE + BALL_RADIUS))

    def ball_hits_paddle(self, paddle):
        # TODO: condition must be True when ball hits the paddle, False otherwise
        return ((paddle.y <= self.ball.y <= paddle.y + PADDLE_HEIGHT) and
                (paddle.x - BALL_RADIUS <= self.ball.x <= paddle.x + PADDLE_WIDTH + BALL_RADIUS))

    def handle_powerup_collision(self):
        self.powerups.activate(self)
        self.powerup_active = True
        self.hide_powerup()

    def handle_paddle_collision(self, paddle):
        # Reverse direction
        self.ball.x_vel *= - 1

        # Change y_vel based on where we hit the paddle
        middle_y = paddle.y + PADDLE_HEIGHT / 2
        difference_y = middle_y - self.ball.y
        reduction_factor = (PADDLE_HEIGHT / 2) / BALL_MAX_VEL
        y_vel = difference_y / reduction_factor
        y_vel = BALL_MAX_VEL if abs(y_vel) > BALL_MAX_VEL else y_vel
        y_vel += random.uniform(-1, 1)  # Avoid endless loops without having to move the paddle
        self.ball.y_vel = -1 * y_vel

    # endregion

    # region TODO (7) Draw the score
    # TODO Score (7) Draw the score
    def draw_score(self):
        # TODO: replace -1 with the correct computations
        one_fourth_window_width = WIN_WIDTH/4
        three_fourths_window_width = WIN_WIDTH * (3/4)

        self.draw_text(str(self.left_score), one_fourth_window_width, 20)
        self.draw_text(str(self.right_score), three_fourths_window_width, 20)

    # endregion

    # region TODO (8) Winning condition
    # TODO Winning condition (8) Draw winning condition
    def draw_winning_text(self, player_name):
        self.draw()
        self.draw_text(player_name + " Player Won", WIN_WIDTH // 2, WIN_HEIGHT // 2 - 90)
        pygame.display.update()
        pygame.time.delay(5000)

    # TODO Winning condition (8) Check if one player has won the game
    def check_winning_condition(self):
        # TODO: replace False with the correct conditions
        left_player_won = self.left_score >= WINNING_SCORE
        right_player_won = self.right_score >= WINNING_SCORE

        # TODO: draw winning text depending on which player won
        if left_player_won:
            self.draw_winning_text("Left")
            return True
        elif right_player_won:
            self.draw_winning_text("Right")
            return True
        else:
            return False

    # endregion

    # region TODO (B) Output handling
    def move_paddle_networks(self, is_left, network_output):
        if network_output == 0:
            # What to do?
            pass

        # 1 means we move upwards
        elif network_output == 1:
            if is_left:
                # What to do?
                self.left_paddle.move(True)
            else:
                # What to do?
                self.right_paddle.move(True)

        # 2 means we move downwards
        else:
            if is_left:
                # What to do?
                self.left_paddle.move(False)
            else:
                # What to do?
                self.right_paddle.move(False)

    # endregion
    def hide_powerup(self):
        self.powerup_visable = False
        self.last_powerup_time = millis()
        pass

    def spawn_new_powerup(self):
        self.powerups_active = False
        self.powerup_visable = True
        self.last_powerup_time = millis()

        pass

def millis():
    return round(time.time() * 1000)