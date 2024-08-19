from operator import abs
from statistics import mean
import time
import numpy as np
import math
from Pong import Game
import neat
import pickle


from Util import load_network_from_file, plot
from Settings import *

mean_fitness_values = []
max_fitness_values = []


# region TODO (A) Training loop
def evaluate_genomes(genomes, config):
    # Initialise fitness
    for ignored, genome in genomes:
        genome.fitness = 0

    # TODO (A) Implement training loop
    for id, genome1 in genomes:
        game = Game(window)
        game.draw()
        train_ai(game, genome1, config)

    # Plots the fitness history
    mean_fitness_values.append(mean([x[1].fitness for x in genomes]))
    max_fitness_values.append(max([x[1].fitness for x in genomes]))
    plot(mean_fitness_values, max_fitness_values)


def move_partner(paddle, ball):
    # TODO (A) Implement training loop
    #  Move the partner paddle with respect to the game state.
    if paddle.y + PADDLE_HEIGHT / 2 < ball.y:
        paddle.move(False)
    else:
        paddle.move(True)
    pass


# endregion


# region TODO (B) Output handling
def train_ai(game, genome1, config):
    run = True
    clock = pygame.time.Clock()
    trainee = neat.nn.FeedForwardNetwork.create(genome1, config)

    reward_multiplier = 1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Move Ball
        game.ball.move()

        # Handle collision
        game.handle_collision()

        # TODO (A) Implement training loop
        #   Move the partner paddle
        move_partner(game.right_paddle, game.ball)

        # TODO (B) Output handling
        #  Move both paddles by querying the networks
        move_paddle_network(game, trainee, game.left_paddle, True)

        # Reset ball if it touches the right or left window border and update the score board.
        if game.ball.x < 0:
            game.right_score = game.right_score + 1
            game.ball.reset()
        elif game.ball.x > WIN_WIDTH:
            game.left_score = game.left_score + 1
            game.ball.reset()

        # Update game screen
        game.draw()

        # TODO (D) Fitness

        if game.left_score == 1 or game.right_score == 1:
            calculate_fitness(genome1, game.left_hits, game)
            break


def move_paddle_network(game, network, paddle, is_left_paddle):
    # TODO (B) Output handling
    #  Move the paddle with respect to the network output
    inputs = get_network_inputs(paddle, game.ball)
    output = network.activate(inputs)

    max_value = 0
    max_index = 0
    current_index = 0
    for output_value in output:
        if output_value > max_value:
            max_value = output_value
            max_index = current_index
        current_index += 1
    game.move_paddle_networks(is_left_paddle, max_index)
    pass

# endregion


def get_network_inputs(paddle, ball):
    # TODO (C) Input handling
    #  Fetch the inputs for our network
    paddle_y = ((paddle.y + PADDLE_HEIGHT // 2) - (WIN_HEIGHT / 2)) / (WIN_HEIGHT / 2)
    ball_y = (ball.y - (WIN_HEIGHT / 2)) / (WIN_HEIGHT / 2)
    xd_paddle_ball = (abs(paddle.x - ball.x) - WIN_WIDTH / 2) / (WIN_WIDTH / 2)

    paddle_y = min(max(paddle_y, -1), 1)
    ball_y = min(max(ball_y, -1), 1)
    xd_paddle_ball = min(max(xd_paddle_ball, -1), 1)

    assert -1 <= paddle_y <= 1, "kek"
    assert -1 <= ball_y <= 1, "kek"
    assert -1 <= xd_paddle_ball <= 1, "kek"

    return [paddle_y, ball_y, xd_paddle_ball]

def calculate_fitness(genome, rewards, game):
    # TODO (D) Fitness
    #  Calculate the fitness of your genome
    genome.fitness = rewards


# region TODO (E) Player vs. NEAT
def play_against_ai(genome, game, config):
    # TODO (E) Player vs. NEAT
    run = True
    clock = pygame.time.Clock()
    network = neat.nn.FeedForwardNetwork.create(genome, config)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Handle collision

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.left_paddle.move(True)
        if keys[pygame.K_s]:
            game.left_paddle.move(False)

        move_paddle_network(game, network, game.right_paddle, False)

        # Move Ball
        game.ball.move()

        game.handle_collision()

        # TODO (B) Output handling
        #  Move both paddles by querying the networks

        # Reset ball if it touches the right or left window border and update the score board.
        if game.ball.x < 0:
            game.right_score = game.right_score + 1
            game.ball.reset()
        elif game.ball.x > WIN_WIDTH:
            game.left_score = game.left_score + 1
            game.ball.reset()

        # Update game screen
        game.draw()

        if game.check_winning_condition():
            run = False
    pass


if __name__ == "__main__":
    # Switch between training mode and single player mode.
    train = True

    # Set the window width and height and initialise the game.
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Set the parameter configuration for NEAT
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "parameter.txt")
    configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    if train:
        pygame.display.set_caption("Training Mode")
        max_generations = 5000

        # Generate initial population. Switch commented lines to start with a new population or load a saved checkpoint.
        population = neat.Population(configuration)
        #population = neat.Checkpointer.restore_checkpoint('Checkpoints/checkpoint-24')

        # Add statistics observer and checkpoints
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(1, filename_prefix="Checkpoints/checkpoint-"))


        # Start Search and save the winner
        winner = population.run(evaluate_genomes, max_generations)
        with open("Networks/Winner.pickle", "wb") as f:
            pickle.dump(winner, f)

    else:
        pygame.display.set_caption("Single Player Mode")
        # Load the opponent
        opponent_path = "Networks/Winner.pickle"
        opponent = load_network_from_file(opponent_path)

        # Start game
        pong = Game(window)
        play_against_ai(opponent, pong, configuration)
# endregion
