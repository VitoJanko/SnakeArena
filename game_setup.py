import random

from ais.ai import AlternativeAI, NoobAI, CuddleAI
from game_objects.snake import Snake

def get_snakes(grid):
    snakes = [
        Snake(
            initial_position=get_random_start(grid),
            direction="RIGHT",
            color=(0, 255, 0),
            grid=grid,
            number=0,
            name="preskok"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="LEFT",
            color=(255, 0, 0),
            grid=grid,
            number=1,
            name="sonce"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="UP",
            color=(0, 0, 255),
            grid=grid,
            number=2,
            name="delo"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="LEFT",
            color=(255, 0, 255),
            grid=grid,
            number=3,
            name="tax-fin-lex"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="LEFT",
            color=(255, 255, 0),
            grid=grid,
            number=4,
            name="aicondition"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="UP",
            color=(0, 255, 255),
            grid=grid,
            number=5,
            name="tenis"
        ),

    ]

    AIs = [AlternativeAI(), NoobAI(), CuddleAI(), AlternativeAI(), NoobAI(), CuddleAI()]
    return snakes, AIs


def get_random_start(grid):
    return random.choice(range(len(grid.grid))), random.choice(range(len(grid.grid[0])))