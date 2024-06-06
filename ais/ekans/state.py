from __future__ import annotations

import itertools

from collections import deque

# from ais.ekans.criterion import CriterionFunction
from game_objects.grid import Grid
from game_objects.snake import Snake
import numpy.typing as npt
import numpy as np


class CriterionFunction:
    num_features: int

    def calculate_features(self, state: State) -> npt.NDArray:
        """
        Function to calculate the features used in determining the
        best move and evaluating the criterion function
        """

        def _compute_radius_density(grid, head, radius):
            our_position_x = head[0]
            our_position_y = head[1]
            return sum(
                grid[our_position_x - radius : our_position_x + radius][
                    our_position_y - radius : our_position_y + radius
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
                if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == 0:
                    escape_routes += 1

            return escape_routes

        def _compute_center_proximity(grid, head):
            rows, cols = len(grid), len(grid[0])
            head_x, head_y = head
            center_x, center_y = cols // 2, rows // 2
            return abs(head_x - center_x) + abs(head_y - center_y)

        def _compute_longest_open_path(grid, head):
            rows, cols = len(grid), len(grid[0])
            head_x, head_y = head
            visited = set()

            def dfs(x, y, length):
                if (
                    not (0 <= x < rows and 0 <= y < cols)
                    or grid[x][y] == 1
                    or (x, y) in visited
                ):
                    return length - 1

                visited.add((x, y))
                max_length = length

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    max_length = max(max_length, dfs(x + dx, y + dy, length + 1))

                visited.remove((x, y))
                return max_length

            return dfs(head_x, head_y, 0)

        def _compute_local_connectivity(grid, head, radius):
            rows, cols = len(grid), len(grid[0])
            head_x, head_y = head
            connectivity = 0

            for i in range(max(0, head_x - radius), min(rows, head_x + radius + 1)):
                for j in range(max(0, head_y - radius), min(cols, head_y + radius + 1)):
                    if grid[i][j] == 0:
                        connected_neighbors = 0
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            if (
                                0 <= i + dx < rows
                                and 0 <= j + dy < cols
                                and grid[i + dx][j + dy] == 0
                            ):
                                connected_neighbors += 1
                        connectivity += connected_neighbors

            return connectivity

        def _calculate_enclosure_params(grid, start):
            rows, cols = len(grid), len(grid[0])
            visited = set()
            queue = deque([start])
            open_space_count = 0

            while queue:
                x, y = queue.popleft()
                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if grid[x][y] == 0:
                    open_space_count += 1
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_x, new_y = x + dx, y + dy
                        if (
                            0 <= new_x < rows
                            and 0 <= new_y < cols
                            and (new_x, new_y) not in visited
                        ):
                            queue.append((new_x, new_y))

            total_open_spaces = sum(cell == 0 for row in grid for cell in row)
            reachable_open_spaces = open_space_count
            return (
                reachable_open_spaces,
                total_open_spaces,
                int(reachable_open_spaces == total_open_spaces),
            )

        our_position = state.position[state.number]

        possible_moves = state.possible_directions
        our_snake_N = state.number
        grid = state.grid.grid
        grid_dangers = [
            [1 if elem is not None else elem for elem in row] for row in grid
        ]
        list_live_snakes = [snake.number for snake in state.snakes if snake.alive == 1]

        # Imminent danger features
        alive = 1 if our_snake_N in list_live_snakes else 0

        print("at escape routes")
        n_escape_routes = _compute_escape_routes(
            grid_dangers, our_position, possible_moves
        )

        print("at density")
        # Abstract/strategic features
        n_square_density = _compute_radius_density(grid, our_position, 1)

        print("at proximity")
        distance_to_center = _compute_center_proximity(grid_dangers, our_position)

        print("at walls")
        distance_to_nearest_wall = _compute_distance_to_walls(
            grid_dangers, our_position
        )
        # longest_open_path = _compute_longest_open_path(grid, our_position)
        longest_open_path = 0

        print("at local")
        n_square_connectivity = _compute_local_connectivity(grid, our_position, 3)

        print("at enclosure")
        (reachable_open_spaces, _, enclosed) = _calculate_enclosure_params(
            grid, our_position
        )

        return np.array(
            [
                alive,
                n_escape_routes,
                n_square_density,
                distance_to_center,
                distance_to_nearest_wall,
                longest_open_path,
                n_square_connectivity,
                reachable_open_spaces,
                enclosed,
            ]
        )

    def evaluate_state(self, state: State, weights: npt.NDArray) -> float:
        return self.calculate_features(state).dot(weights)


class State:
    def __init__(
        self,
        grid: Grid,
        number: int,
        position: dict[int, tuple[int, int]],
        current_direction: str,
        possible_directions: list[str],
        snakes: list[Snake],
    ):
        self.grid = grid
        self.number = number  # zaporedna številka kače
        self.position = position  # {0: (29, 32), 1: (4, 15), 2: (23, 26), 3: (15, 9), 4: (17, 26)}  - glave od kač
        self.current_direction = current_direction  # "LEFT" -> kam si sel nazadnje
        self.possible_directions = possible_directions  # ["LEFT", "RIGHT", "UP"]
        self.snakes = snakes  # sezname vseh kač

    def resolve_action(self, active_snake: int, chosen_direction: str) -> None:
        snake = get_snake_numbered(active_snake, self.snakes)
        snake.direction = chosen_direction
        self.current_direction = chosen_direction

        if snake.alive:
            snake.special_move("turbo")
            snake.move()
            if self.grid.check_collision(snake):
                snake.alive = False
            snake.grid.update_snake_position(snake)

    # def resolve_action(self):
    #     for snake in self.snakes:
    #         self.make_move(snake.number, snake.direction)
    #         if snake.number == self.number:
    #             self.grid = snake.grid


def search_for_move(
    current_state: State, active_snake: int, look_ahead: int, weights: npt.NDArray
) -> str:
    possible_moves = current_state.possible_directions
    initial_state = current_state

    best_move = None
    best_score = float("-inf")

    options = ["LEFT", "RIGHT", "UP", "DOWN"]
    all_possibilities = itertools.product([options] * look_ahead)

    for possibility in all_possibilities:
        current_state = initial_state
        for move in possibility:
            if move not in current_state.possible_directions:
                break
            current_state = current_state.resolve_action(active_snake, move)
        print("evaluating")
        score = CriterionFunction().evaluate_state(current_state, weights)
        if score > best_score:
            best_score = score
            best_move = possibility[0]
    return best_move


def get_snake_numbered(number: int, snakes: list[Snake]) -> Snake:
    for snake in snakes:
        if snake.number == number:
            return snake
