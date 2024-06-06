import random
from game_objects.snake import Snake
from constants import DIRECTIONS


class BaseAI:

    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        return random.choice(possible_directions)


class NoobAI:

    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        position = positions[number]
        head_x, head_y = position
        direction = possible_directions[0]
        for _ in range(15):
            direction = random.choice(possible_directions)
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (head_x + dir_x, head_y + dir_y)
            if not collision(new_head[0], new_head[1], grid):
                break
        return direction


class AlternativeAI:

    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        position = positions[number]
        head_x, head_y = position
        direction = current_direction
        dir_x, dir_y = DIRECTIONS[direction]
        new_head = (head_x + dir_x, head_y + dir_y)
        if not collision(new_head[0], new_head[1], grid):
            return direction

        for _ in range(15):
            direction = random.choice(possible_directions)
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (head_x + dir_x, head_y + dir_y)
            if not collision(new_head[0], new_head[1], grid):
                break

        return direction


class CuddleAI:
    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        position = positions[number]
        possibilities = []
        for direction in possible_directions:
            dir_x, dir_y = DIRECTIONS[direction]
            new_head = (position[0] + dir_x, position[1] + dir_y)
            if collision(new_head[0], new_head[1], grid):
                possibilities.append((direction, -100))
            else:
                possibilities.append((direction, number_of_neighbors(new_head[0], new_head[1], grid, number)))
        possibilities.sort(key=lambda x: x[1], reverse=True)
        return possibilities[0][0]


def collision(head_x, head_y, grid):
    if head_x < 0 or head_x >= len(grid) or head_y < 0 or head_y >= len(grid[0]):
        return True
    if grid[head_x][head_y] is not None:
        return True
    return False


def number_of_neighbors(head_x, head_y, grid, number):
    neighbors = 0
    for direction in DIRECTIONS.values():
        new_x = head_x + direction[0]
        new_y = head_y + direction[1]
        if new_x < 0 or new_x >= len(grid) or new_y < 0 or new_y >= len(grid[0]):
            continue
        if grid[new_x][new_y] == number:
            neighbors += 1
    return neighbors
