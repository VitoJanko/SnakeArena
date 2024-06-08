import random

import numpy as np
from collections import deque

from ais.ai import collision
from constants import DIRECTIONS
from game_objects.snake import Snake


def count_reachable_tiles(grid, start_position, return_reachable=False):
    rows, cols = grid.shape
    start_row, start_col = start_position

    if not grid[start_row, start_col]:
        return 0

    visited = np.zeros_like(grid, dtype=bool)
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True
    reachable_count = 0

    while queue:
        current_row, current_col = queue.popleft()
        reachable_count += 1

        for dr, dc in DIRECTIONS.values():
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row, new_col] and not visited[new_row, new_col]:
                    visited[new_row, new_col] = True
                    queue.append((new_row, new_col))
    if return_reachable:
        reachable = []
        for row in range(rows):
            for col in range(cols):
                if visited[row, col]:
                    reachable.append((row, col))
        return reachable
    return reachable_count


class SpaceCountAI:
    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        for snake in snakes:
            if snake.number == number and not snake.alive:
                breakpoint()
        position = positions[number]
        possibilities = []
        grid_np = np.equal(np.array(grid), None)

        for direction in possible_directions:
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (position[0] + dir_x, position[1] + dir_y)
            if collision(new_head[0], new_head[1], grid):
                possibilities.append((direction, -100))
            else:
                possibilities.append((direction,  count_reachable_tiles(grid_np, new_head)))
        possibilities.sort(key=lambda x: x[1], reverse=True)
        return possibilities[0][0]


class SpaceBlockerAI:
    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        position = positions[number]
        possibilities = []
        snakes_dict = {snake.number: snake for snake in snakes}

        for direction in possible_directions:
            grid_np = np.equal(np.array(grid), None)
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (position[0] + dir_x, position[1] + dir_y)

            closeness_penalty = 0
            for snake_num, snake_position in positions.items():
                if snake_num != number and snakes_dict[snake_num].alive:
                    # print(abs(new_head[0] - snake_position[0]) + abs(new_head[1] - snake_position[1]))
                    if abs(new_head[0] - snake_position[0]) + abs(new_head[1] - snake_position[1]) <= 2:
                        closeness_penalty = max(closeness_penalty, 2)
                    if abs(new_head[0] - snake_position[0]) + abs(new_head[1] - snake_position[1]) <= 5:
                        closeness_penalty = max(closeness_penalty, 1)
            # print(closeness_penalty)

            if collision(new_head[0], new_head[1], grid):
                possibilities.append((direction, -10000))
            else:
                reachable = count_reachable_tiles(grid_np, new_head)
                reachable_tiles = []
                for snake_num, snake_position in positions.items():
                    if snake_num != number and snakes_dict[snake_num].alive:
                        grid_np[snake_position[0], snake_position[1]] = True
                        grid_np[new_head[0], new_head[1]] = False
                        reachable_tiles.append(count_reachable_tiles(grid_np, snake_position))
                opponent_can_reach = 0
                if len(reachable_tiles) > 0:
                    opponent_can_reach = max(reachable_tiles) / len(reachable_tiles)
                score = reachable - opponent_can_reach + random.random() -closeness_penalty
                possibilities.append((direction,  score))
        possibilities.sort(key=lambda x: x[1], reverse=True)
        # print("---")
        return possibilities[0][0]


class TwoFaceAI:
    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        others_reachable = False
        grid_np = np.equal(np.array(grid), None)
        for position in positions.values():
            grid_np[position[0], position[1]] = True
        reachable = count_reachable_tiles(grid_np, positions[number], return_reachable=True)
        positions_to_search = [pos for (num, pos) in positions.items() if num != number]
        for field in reachable:
            if field in positions_to_search:
                others_reachable = True
                break
        if others_reachable:
            return SpaceBlockerAI().get_direction(grid, number, positions, current_direction, possible_directions, snakes)
        else:
            return SpaceCountAI().get_direction(grid, number, positions, current_direction, possible_directions, snakes)


class MonteAI:
    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        position = positions[number]
        possibilities = []
        snakes_dict = {snake.number: snake for snake in snakes}

        for direction in possible_directions:
            grid_np = np.equal(np.array(grid), None)
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (position[0] + dir_x, position[1] + dir_y)
            closeness_penalty = 0
            for snake_num, snake_position in positions.items():
                if snake_num != number and snakes_dict[snake_num].alive:
                    if abs(new_head[0] - snake_position[0]) + abs(new_head[1] - snake_position[1]) <= 1:
                        closeness_penalty = max(closeness_penalty, 2)
                    if abs(new_head[0] - snake_position[0]) + abs(new_head[1] - snake_position[1]) <= 2:
                        closeness_penalty = max(closeness_penalty, 1)
            if collision(new_head[0], new_head[1], grid):
                possibilities.append((direction, -10000))
            else:
                max_score = -9999
                reachable = count_reachable_tiles(grid_np, new_head)
                for _ in range(5):
                    test_head = tuple(new_head)
                    grid_np = np.equal(np.array(grid), None)
                    for move in range(max(0, min(10, reachable-1))):
                        new_direction, collided = choose_move(grid_np, test_head, DIRECTIONS.keys())
                        if collided:
                            max_score = max(max_score, -9999 + move)
                            break
                        grid_np[test_head[0], test_head[1]] = False
                        test_head = (test_head[0] + DIRECTIONS[new_direction][0], test_head[1] + DIRECTIONS[new_direction][1])

                    reachable = count_reachable_tiles(grid_np, new_head)
                    reachable_tiles = []
                    for snake_num, snake_position in positions.items():
                        if snake_num != number and snakes_dict[snake_num].alive:
                            grid_np[snake_position[0], snake_position[1]] = True
                            grid_np[new_head[0], new_head[1]] = False
                            reachable_tiles.append(count_reachable_tiles(grid_np, snake_position))
                    opponent_can_reach = 0
                    if len(reachable_tiles) > 0:
                        opponent_can_reach = max(reachable_tiles) / len(reachable_tiles)
                    score = reachable - opponent_can_reach + random.random() - closeness_penalty
                    max_score = max(max_score, score)
                possibilities.append((direction, max_score))
        possibilities.sort(key=lambda x: x[1], reverse=True)
        # print(possibilities)
        return possibilities[0][0]


def choose_move(grid, position, possible_directions):
    non_collision = []
    for direction in possible_directions:
        dir_x, dir_y = DIRECTIONS[direction]
        new_head = (position[0] + dir_x, position[1] + dir_y)
        if not collision_np(new_head[0], new_head[1], grid):
            non_collision.append(direction)
    if len(non_collision) == 0:
        return None, True
    else:
        return random.choice(non_collision), False


def collision_np(head_x, head_y, grid):
    if head_x < 0 or head_x >= grid.shape[0] or head_y < 0 or head_y >= grid.shape[1]:
        return True
    if grid[head_x, head_y] is not None:
        return True
    return False
