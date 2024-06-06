import random

from ais.ai import AlternativeAI, NoobAI, CuddleAI, QueenAI
from constants import DIRECTIONS
from game_objects.snake import Snake


def get_snakes(grid):
    snakes = [
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(0, 255, 0),
            grid=grid,
            number=0,
            name="preskok"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(255, 0, 0),
            grid=grid,
            number=1,
            name="sonce"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(0, 0, 255),
            grid=grid,
            number=2,
            name="delo"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(255, 0, 255),
            grid=grid,
            number=3,
            name="tax-fin-lex"
        ),


    ]

    AIs = [QueenAI(), NoobAI(), CuddleAI(), AlternativeAI(),]
    return snakes, AIs


def get_random_start(grid):
    return random.choice(range(2, len(grid.grid[0])-2)), random.choice(range(2, len(grid.grid)-2))