import numpy as np
from ais.ekans.state import State, search_for_move
from game_objects.grid import Grid
from ais.ai import BaseAI, CuddleAI
from game_objects.snake import Snake
from constants import GRID_WIDTH, GRID_HEIGHT


class EkansAI(CuddleAI):
    pass


class EkansAI2(BaseAI):
    def __init__(self):
        self.weights = np.array([1000, 1, 1, 0, 1, 1, 1, 1, -1])

    def get_direction(
        self,
        grid,
        number,
        positions,
        current_direction,
        possible_directions,
        snakes: list[Snake],
    ):
        print("razmišljam")
        grid_obj = Grid(GRID_WIDTH, GRID_HEIGHT)
        grid_obj.grid = grid

        state = State(
            grid_obj, number, positions, current_direction, possible_directions, snakes
        )
        print("starting search")
        move = search_for_move(state, number, 3, self.weights)
        print("move found")
        return move
