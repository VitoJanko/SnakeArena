from constants import DIRECTIONS
from game_objects.snake import Snake


class PreskokSnake (Snake):
    def __init__(self, initial_position, direction, number, grid, color=(0, 0, 0)):
        super().__init__(initial_position, direction, number, grid, color)
        self.turbo = False

    def special_move(self, command):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.active > 0:
            self.active -= 1
        elif self.active == 0:
            self.turbo = False
        if self.cooldown == 0 and command == "turbo":
            self.turbo = True
            self.active = 7
            self.cooldown = 21

    def move(self):
        self.also_check = []
        head_x, head_y = self.body[0]
        dir_x, dir_y = DIRECTIONS[self.direction]
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body
        if self.turbo:
            self.also_check = [new_head]
            new_head = (new_head[0] + dir_x, new_head[1] + dir_y)
            self.body = [new_head] + self.body

