from constants import DIRECTIONS
from game_objects.grid import Grid


class Snake:
    def __init__(self, initial_position, direction, number, grid: Grid, color=(0, 0, 0), name="sonce"):
        self.body = [initial_position]
        self.direction = direction
        self.color = color
        self.alive = True
        self.number = number
        self.grid = grid
        self.cooldown = 0
        self.active = 0
        self.also_check = []
        self.name = name
        self.score = 0

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = DIRECTIONS[self.direction]
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body

    def special_move(self, command):
        pass

    def get_head_position(self):
        return self.body[0]

    def get_possible_directions(self):
        if self.direction in ["UP"]:
            return ["LEFT", "RIGHT", "UP"]
        if self.direction in ["DOWN"]:
            return ["LEFT", "RIGHT", "DOWN"]
        if self.direction in ["LEFT"]:
            return ["UP", "DOWN", "LEFT"]
        if self.direction in ["RIGHT"]:
            return ["UP", "DOWN", "RIGHT"]
