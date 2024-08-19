import pygame
from Settings import *


class Paddle:
    def __init__(self,window,x,y,color):
        self.x = x
        self.y = y
        self.window = window
        self.color = color
        pass
    def draw(self):
        # TODO Paddle (1) Draw the paddles
        #  Which shape has a paddle and how can we draw it?
        pygame.draw.rect(self.window, self.color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pass

    def move(self, upwards):
        # TODO Paddle (2) Move the paddles
        if(upwards):
            new_pos = self.y -PADDLE_VEL
            min_pos = 0
            if new_pos < min_pos:
                self.y = min_pos
            else:
                self.y = new_pos

        else:
            new_pos = self.y +PADDLE_VEL
            min_pos = WIN_HEIGHT-PADDLE_HEIGHT
            if new_pos > min_pos:
                self.y = min_pos
            else:
                self.y = new_pos
            
        #  How can we move the paddles?
        #  If we move the paddles, we have to make sure they stay within the window.
        pass
