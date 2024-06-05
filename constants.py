GRID_WIDTH = 50
GRID_HEIGHT = 50
CELL_SIZE = 20

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + 250  # Extra space for the score
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}