import math
import random
import pygame

from Settings import *


class Ball:

    def __init__(self,window,x,y,color):
        self.window = window
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.color = color
        self.x_vel, self.y_vel = self.define_starting_direction()
        # Which attributes do we need for the Ball?

        pass

    def draw(self):
        # TODO Ball (3) Draw the ball
        pygame.draw.circle(self.window,self.color,(self.x,self.y),BALL_RADIUS)
        #  Which shape has a ball and how can we draw it?
        pass

    def move(self):
        # TODO Ball (4) Move the ball
        self.y += self.y_vel
        self.x += self.x_vel
        #  How can we move the ball? Hint: We need a separate velocity in x and y direction.
        pass

    def reset(self):
        # TODO Ball (5) Reset the ball
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel, self.y_vel = self.define_starting_direction()
        #  Which attributes may change and have to be reset?
        pass

    def define_starting_direction(self):
        # Defines a random starting direction of the ball.
        angle = 0
        while angle == 0:
            angle = math.radians(random.randrange(-30, 30))
        pos = 1 if random.random() < 0.5 else -1
        x_vel = pos * abs(math.cos(angle) * BALL_MAX_VEL)
        y_vel = math.sin(angle) * BALL_MAX_VEL
        return x_vel, y_vel

    # Used for powerups
    def change_speed(self, delta):
        # Change the speed of the ball in x and y direction by the specified delta
        if self.x_vel < 0:
            self.x_vel -= delta
        else:
            self.x_vel += delta

        if self.y_vel < 0:
            self.y_vel -= delta
        else:
            self.y_vel += delta
        pass
