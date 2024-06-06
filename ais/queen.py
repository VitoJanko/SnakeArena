import random
import numpy as np
import math

from game_objects.snake import Snake
from constants import DIRECTIONS


class QueenAI:
    
    W_OCCUPANCY = 9
    W_DISTANCE = 1
    AMOUNT_OF_SPLITS = 4

    def get_direction(self, grid, number, positions, current_direction, possible_directions, snakes: list[Snake]):
        grid = np.array(grid)
        head_position = positions[number]
        head_x, head_y = head_position
        subgrid_center = self.find_empty_space(grid, head_position, self.AMOUNT_OF_SPLITS)
        if head_x > subgrid_center[0]:
            x_dir = "LEFT"
        else:
            x_dir = "RIGHT"

        if head_y > subgrid_center[1]:
            y_dir = "UP"
        else:
            y_dir = "DOWN"

        x_diff = abs(head_x - subgrid_center[0])
        y_diff = abs(head_y - subgrid_center[1])
        
        # TODO
        next_directions = self.possible_moves(grid, head_position, possible_directions)
        
        # print(x_dir, y_dir)
        # print(next_directions)
        
        next_move = None

        if (x_diff <= y_diff):
            if (y_dir in next_directions):
                next_move = y_dir
            elif x_dir in next_directions:
                next_move = x_dir
        else: 
            if (x_dir in next_directions):
                next_move = x_dir
            elif y_dir in next_directions:
                next_move = y_dir

        if next_move is None:
            if len(next_directions) > 0:
                next_move = next_directions[0]
            else:
                next_move = current_direction
        # print("Next move: ", next_move)
        return next_move
    
    def possible_moves(self, grid, head_position, possible_directions):
        moves = []
        x_length = np.shape(grid)[0]
        y_length = np.shape(grid)[1]
        for direction in possible_directions:
            if direction == "DOWN":
                if (head_position[1]+1) < y_length:
                    if grid[head_position[0], head_position[1]+1] is None:
                        moves.append("DOWN")
            if direction == "UP":
                if (head_position[1]-1) >= 0:
                    if grid[head_position[0], head_position[1]-1] is None:
                        moves.append("UP")
            if direction == "RIGHT":
                if (head_position[0]+1) < x_length:
                    if grid[head_position[0]+1, head_position[1]] is None:
                        moves.append("RIGHT")
            if direction == "LEFT":
                if (head_position[0]-1) >= 0:
                    if grid[head_position[0]-1, head_position[1]] is None:
                        moves.append("LEFT")
        return moves

    def calculate_score(self, subgrid, subgrid_center, head_position):
        distance = np.abs(head_position[0] - subgrid_center[0]) + np.abs(head_position[1] - subgrid_center[1])
        return np.count_nonzero(subgrid == None)* self.W_OCCUPANCY + distance * self.W_DISTANCE
    
    def find_empty_space(self, grid, head_position, amount_of_splits):
        x_length, y_length = np.shape(grid)
        if x_length >= y_length:
            axis = 0
        else:
            axis = 1

        best_score = 100000
        best_subgrid_center = None

        x_step = (x_length//amount_of_splits)
        y_step = (y_length//amount_of_splits)

        for split_x in range(amount_of_splits):
            x_left = split_x*x_step
            x_right = min(x_left + x_step, x_length)
            for split_y in range(amount_of_splits):
                y_top = split_y*y_step
                y_bottom = min(split_y*y_step, y_length)
                
                subgrid = grid[x_left:x_right, y_top:y_bottom]

                subgrid_center = ((x_right+x_left)//2, (y_top+y_bottom)//2)
                score = self.calculate_score(subgrid, subgrid_center, head_position)

                if score < best_score:
                    best_score = score
                    best_subgrid_center = subgrid_center
        
        return best_subgrid_center
