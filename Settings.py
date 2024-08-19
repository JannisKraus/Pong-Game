import datetime
import os

import pygame

pygame.init()

# Game Settings
WIN_WIDTH, WIN_HEIGHT = 700, 500
FPS = 60
FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

# Color converter: https://www.rapidtables.com/convert/color/rgb-to-hex.html
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Decide if you want to use a background image.
BG_IMG = None#pygame.transform.scale(pygame.image.load(os.path.join("img", "Soccer.png")), (WIN_WIDTH, WIN_HEIGHT))
#BG_IMG = None

# Paddle Settings
PADDLE_VEL = 5
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# Ball Settings
BALL_MAX_VEL = 7
BALL_RADIUS = 7

# Powerup Settings
POWERUPS_ENABLED = True
POWERUP_SIZE = BALL_RADIUS * 7
POWERUP_SPAWN_DELAY = 10_000
POWERUP_DISPLAY_TIME = 15_000
POWERUP_DURATION = 10_000
# POWERUP_BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "Powerup.png")), (POWERUP_SIZE, POWERUP_SIZE))
POWERUP_BG_IMG = None
ENABLED_POWERUPS = [
    # Add custom powerups to this list
    "FastBall",
    "FastPaddle",
]
