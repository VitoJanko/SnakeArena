from copy import deepcopy
import numpy as np

from .ai import BaseAI, collision
from constants import DIRECTIONS


class PitoniAI(BaseAI):
    def get_direction(
        self,
        grid,
        number,
        positions,
        current_direction,
        possible_directions,
        snakes,
    ):
        possibilities = self.optimize(
            grid,
            number,
            positions,
            possible_directions,
            max_recursion_depth=5,
            steps=[],
            step_weights=[],
            position=positions[number],
        )
        possibilities.sort(key=lambda x: (x[1], -x[2]), reverse=True)
        return possibilities[0][0][0]

    def optimize(
        self,
        grid,
        number,
        positions,
        possible_directions,
        max_recursion_depth,
        steps,
        step_weights,
        position,
    ):
        if max_recursion_depth == 0:
            return [(steps, len(steps), sum(step_weights))]

        possibilities = []
        best_weight = 1
        for direction in possible_directions:
            weight = 1
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (position[0] + dir_x, position[1] + dir_y)
            new_steps = steps + [direction]
            if not collision(new_head[0], new_head[1], grid):
                aux_grid = deepcopy(grid)
                aux_grid[new_head[0]][new_head[1]] = number

                weight = weight_of_step(
                    grid, new_head, positions, number, len(new_steps)
                )
            best_weight = min(best_weight, weight)

            if (weight > best_weight * 0.7 and weight < 1) or weight < 0.3:
                possibilities += self.optimize(
                    aux_grid,
                    number,
                    positions,
                    possible_directions,
                    max_recursion_depth - 1,
                    new_steps,
                    step_weights + [weight],
                    new_head,
                )
            else:
                possibilities.append(
                    (
                        new_steps,
                        len(new_steps),
                        sum(step_weights),
                    )
                )
        return possibilities


def get_snake_paths(grid, x, y, num_steps, steps, head, first=True):
    if not first and (num_steps == 0 or collision(x, y, grid)) or (x, y) == head:
        return [steps]

    aux_grid = deepcopy(grid)
    aux_grid[x][y] = 1
    possibilities = []
    for dx, dy in DIRECTIONS.values():
        new_x = x + dx
        new_y = y + dy
        possibilities += get_snake_paths(
            aux_grid,
            new_x,
            new_y,
            num_steps - 1,
            steps + [(new_x, new_y)],
            head,
            first=False,
        )
    return possibilities


def weight_of_step(grid, head, positions, number, num_steps):
    probability = 0
    for i, position_i in positions.items():
        if (
            i != number
            and head[0] - num_steps < position_i[0] < head[0] + num_steps
            and head[1] - num_steps < position_i[1] < head[1] + num_steps
        ):
            probability += 1 / np.sqrt(
                (np.abs(position_i[0] - head[0]) * np.abs(position_i[1] - head[1]))
                + 1e-1
            )
    return probability