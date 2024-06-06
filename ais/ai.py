import random

from constants import DIRECTIONS
from game_objects.snake import Snake
from copy import deepcopy

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
    
    
NUM_MOVES = 50
class CuddleAI:
    def get_direction_internal(self, grid, number, position, current_direction, possible_directions):
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
    
    def dummy(self, grid, number, positions, possible_directions):
        print(positions)
        position = positions[number] 
        for i in range(NUM_MOVES):
            position_str = self.get_direction_internal(grid, number, position, None, possible_directions) 
            xd, yd = DIRECTIONS[position_str]
            new_head = (position[0] + xd, position[1] + yd)
            
            if collision(new_head[0], new_head[1], grid):
                return i
            grid[new_head[0]][new_head[1]] = number
            position = new_head
        return NUM_MOVES

    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes):
   
        moves_dict = []
        
        for possible_direction in possible_directions:
            backup_grid = deepcopy(grid)
            num_moves = self.dummy(backup_grid, number, positions, DIRECTIONS.keys())
            
            moves_dict.append((possible_direction, num_moves))
            
        moves_dict.sort(key=lambda x: x[1], reverse=True)
        
        best_move=moves_dict[0]
 
        default_move =  self.get_direction_internal(grid, number, positions[number], current_direction, possible_directions)         
        
        sum = 0
        for move in moves_dict:
            sum += move[1]
            
        if sum == 3*NUM_MOVES:
            return default_move
        else:
            return best_move[0]



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
