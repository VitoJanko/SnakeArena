import pygame
import time
from constants import GRID_WIDTH, GRID_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, MAX_ROUNDS
from drawing import draw_grid, draw_snake, load_images, draw_scores
from game_objects.grid import Grid
from game_setup import get_snakes


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    load_images(pygame)

    font = pygame.font.Font(None, 36)
    iteration = 0
    running = True
    current_round = 0

    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    snakes, ais = get_snakes(grid)
    debug = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move snakes
        extra_collision = []
        for snake in snakes:
            if snake.alive:
                snake.move()
                extra_collision.append(snake.get_head_position())

        index = 0
        for snake in snakes:
            if snake.alive:
                if grid.check_collision(snake, extra_collision, index):
                    snake.alive = False
                index += 1

        for snake in snakes:
            if snake.alive:
                snake.grid.update_snake_position(snake)

        # Draw everything
        screen.fill((0, 0, 0))
        draw_grid(screen, pygame)
        draw_scores(screen, snakes, font)
        new_grid = grid.get_grid()
        for i, (AI, snake) in enumerate(zip(ais, snakes)):
            draw_snake(screen, snake, pygame)
            if snake.alive:
                start = time.time()
                possible_directions = snake.get_possible_directions()
                direction = AI.get_direction(
                    new_grid,
                    snake.number,
                    {snake.number: snake.get_head_position() for snake in snakes},
                    snake.direction,
                    possible_directions,
                    snakes,
                )
                end = time.time()
                if debug:
                    print(snake.name, int((end - start)*1000))
                if direction in possible_directions:
                    snake.direction = direction
        snakes_alive = [snake for snake in snakes if snake.alive]
        iteration += 1
        if len(snakes_alive) <= 1:
            if len(snakes_alive) == 1:
                snakes_alive[0].score += 1
                current_round += 1

            snakes_old = snakes
            grid = Grid(GRID_WIDTH, GRID_HEIGHT)
            snakes, ais = get_snakes(grid)
            for snake_new, snake_old in zip(snakes, snakes_old):
                snake_new.score = snake_old.score

            if current_round >= MAX_ROUNDS:
                breakpoint()

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


main()
