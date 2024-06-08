import random

from ais.ai import AlternativeAI, NoobAI, CuddleAI
from ais.ekans.main import EkansAI
from ais.monte_ai import SpaceCountAI, SpaceBlockerAI, MonteAI, TwoFaceAI
from ais.pitoni import PitoniAI
from ais.poolai import PoolAI
from constants import DIRECTIONS
from game_objects.snake import Snake



def get_snakes(grid):
    snakes = [
        # Snake(
        #     initial_position=get_random_start(grid),
        #     direction=random.choice(list(DIRECTIONS.keys())),
        #     color=(0, 255, 0),
        #     grid=grid,
        #     number=0,
        #     name="SmallSnake"
        # ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(255, 0, 0),
            grid=grid,
            number=1,
            name="EkansAI"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(0, 0, 255),
            grid=grid,
            number=2,
            name="PitoniAI"
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(255, 0, 255),
            grid=grid,
            number=3,
            name="PoolAI"
        ),

        Snake(
            initial_position=get_random_start(grid),
            direction=random.choice(list(DIRECTIONS.keys())),
            color=(255, 255, 0),
            grid=grid,
            number=4,
            name="TwoFace"
        ),

    ]

    AIs = [EkansAI(), PitoniAI(), PoolAI(), TwoFaceAI()]
    return snakes, AIs


def get_random_start(grid):
    return random.choice(range(2, len(grid.grid[0])-2)), random.choice(range(2, len(grid.grid)-2))