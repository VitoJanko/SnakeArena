from constants import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE
from game_objects.snake import Snake

head_icons = None

def load_images(pygame):
    global  head_icons
    head_icons = {
        "delo": pygame.image.load("./images/1.png"),
        "preskok": pygame.image.load("./images/2.png"),
        "sonce": pygame.image.load("./images/3.png"),
        "tenis": pygame.image.load("./images/4.png"),
        "tax-fin-lex": pygame.image.load("./images/5.png"),
        "aicondition": pygame.image.load("./images/6.png"),
    }

def draw_grid(screen, pygame):
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)


def draw_snake(screen, snake: Snake, pygame):
    for i, segment in enumerate(snake.body):

        color = snake.color
        if not snake.alive:
            color = (
                max(snake.color[0] - 100, 0),
                max(snake.color[1] - 100, 0),
                max(snake.color[2] - 100, 0)
            )

        x = segment[0]
        y = segment[1]
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 0), rect)

        inner_rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(screen, color, inner_rect)

        if i > 0:
            prev_x, prev_y = snake.body[i - 1]
            if prev_x == x:
                # Vertical connection
                connector_rect = pygame.Rect(
                    x * CELL_SIZE + 2, min(y, prev_y) * CELL_SIZE + CELL_SIZE - 2,
                    CELL_SIZE - 4, 4)
            elif prev_y == y:
                # Horizontal connection
                connector_rect = pygame.Rect(
                    min(x, prev_x) * CELL_SIZE + CELL_SIZE - 2, y * CELL_SIZE + 2,
                    4, CELL_SIZE - 4)
            pygame.draw.rect(screen, color, connector_rect)

        if i== 0:
            head_icon = head_icons[snake.name]
            head_icon = pygame.transform.scale(head_icon, (CELL_SIZE, CELL_SIZE))
            screen.blit(head_icon, (x * CELL_SIZE, y * CELL_SIZE))


def draw_scores(screen, snakes: list[Snake], font):
    for i, snake in enumerate(snakes):
        score_text = f"{snake.name.upper()}: {snake.score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, (GRID_WIDTH * CELL_SIZE + 20, 20 + i * 60))