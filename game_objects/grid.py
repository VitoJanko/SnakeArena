class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def update_snake_position(self, snake, remove=False):
        if not snake.alive:
            return
        for segment in snake.body:
            x, y = segment
            self.grid[y][x] = snake

    def check_collision(self, snake, extra_collision, number):
        extra_collision = extra_collision[:number] + extra_collision[number+1:]
        collision = any(
            [
                self.check_one_collision(segment, extra_collision)
                for segment in snake.also_check + [snake.get_head_position()]
            ]
        )
        return collision

    def check_one_collision(self, position, extra_collision):
        head_x, head_y = position
        if position in extra_collision:
            return True
        # Check wall collision
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            return True
        # Check collision with other snakes or itself
        if self.grid[head_y][head_x] is not None:
            return True
        return False

    def get_grid(self):
        grid = [
            [
                self.grid[i][j].number if self.grid[i][j] is not None else None
                for i in range(self.height)
            ]
            for j in range(self.width)
        ]
        return grid
