import pygame

from constants import GRID_WIDTH, GRID_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, MAX_ROUNDS
from drawing import draw_grid, draw_snake, load_images, draw_scores
from game_objects.grid import Grid
from game_setup import get_snakes


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    load_images(pygame)

    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    snakes = None
    font = pygame.font.Font(None, 36)
    iteration = 0
    running = True
    current_round = 0

    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    snakes, ais = get_snakes(grid)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move snakes
        for snake in snakes:
            if snake.alive:
                snake.special_move("turbo")
                snake.move()
                if grid.check_collision(snake):
                    snake.alive = False
                snake.grid.update_snake_position(snake)

        # Draw everything
        screen.fill((0, 0, 0))
        draw_grid(screen, pygame)
        draw_scores(screen, snakes, font)
        new_grid = grid.get_grid()
        for AI, snake in zip(ais, snakes):
            draw_snake(screen, snake, pygame)
            if snake.alive:
                possible_directions = snake.get_possible_directions()
                direction = AI.get_direction(
                    new_grid,
                    snake.number,
                    {snake.number: snake.get_head_position() for snake in snakes},
                    snake.direction,
                    possible_directions
                )
                if direction in possible_directions:
                    snake.direction = direction
        snakes_alive = [snake for snake in snakes if snake.alive]
        iteration += 1
        if len(snakes_alive) <= 0:
            if len(snakes_alive) == 0:
                snakes_alive[0].score += 1

            snakes_old = snakes
            grid = Grid(GRID_WIDTH, GRID_HEIGHT)
            snakes, ais = get_snakes(grid)
            for snake_new, snake_old in zip(snakes, snakes_old):
                snake_new.score = snake_old.score
            current_round +=1
            if current_round <= MAX_ROUNDS:
                break

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


main()
