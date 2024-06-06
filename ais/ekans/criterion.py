import numpy as np

from ais.ekans.state import State
import numpy.typing as npt
from collections import deque


class CriterionFunction:
    num_features: int

    def calculate_features(self, state: State) -> npt.NDArray:
        """
        Function to calculate the features used in determining the
        best move and evaluating the criterion function
        """

        def _compute_radius_density(grid, head, radius):
            our_position_x = our_position[0]
            our_position_y = our_position[1]
            return sum(
                grid_dangers[
                    our_position_x - radius : our_position_x + radius,
                    our_position_y - radius : our_position_y + radius,
                ]
            )

        def _compute_distance_to_walls(grid, head):
            rows, cols = len(grid), len(grid[0])
            head_x, head_y = head
            distance_to_top_wall = head_x
            distance_to_bottom_wall = rows - head_x - 1
            distance_to_left_wall = head_y
            distance_to_right_wall = cols - head_y - 1

            return min(
                distance_to_top_wall,
                distance_to_bottom_wall,
                distance_to_left_wall,
                distance_to_right_wall,
            )

        def _compute_escape_routes(grid, head, possible_moves):
            move_mapping = {
                "LEFT": (-1, 0),
                "RIGHT": (1, 0),
                "UP": (0, 1),
                "DOWN": (0, -1),
            }
            possible_moves_tuple = [move_mapping[move] for move in possible_moves]
            rows, cols = len(grid), len(grid[0])
            head_x, head_y = head
            escape_routes = 0

            for dx, dy in possible_moves_tuple:
                new_x, new_y = head_x + dx, head_y + dy
                ...

    def evaluate_state(self, state: State, weights: npt.NDArray) -> float:
        return self.calculate_features(state).dot(weights)
