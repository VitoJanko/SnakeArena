import pygame
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy

from constants import GRID_WIDTH, GRID_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, MAX_ROUNDS
from drawing import draw_grid, draw_snake, load_images, draw_scores
from game_objects.grid import Grid
from game_setup import get_snakes

def run_single_simulation(simulation_id):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    load_images(pygame)
    font = pygame.font.Font(None, 36)

    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    snakes, ais = get_snakes(grid)
    win_counts = {snake.number: 0 for snake in snakes}

    current_round = 0
    while current_round < MAX_ROUNDS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return win_counts

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
                    possible_directions,
                    snakes,
                )
                if direction in possible_directions:
                    snake.direction = direction

        snakes_alive = [snake for snake in snakes if snake.alive]
        if len(snakes_alive) <= 1:
            if len(snakes_alive) == 1:
                snakes_alive[0].score += 1
                win_counts[snakes_alive[0].number] += 1

            # Reset grid and snakes for the next round
            grid = Grid(GRID_WIDTH, GRID_HEIGHT)
            new_snakes, ais = get_snakes(grid)
            for snake_new, snake_old in zip(new_snakes, snakes):
                snake_new.score = snake_old.score
            snakes = new_snakes

            current_round += 1

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    return win_counts

def run_parallel_simulations(num_simulations=100):
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_single_simulation, i) for i in range(num_simulations)]
        results = [future.result() for future in as_completed(futures)]

    total_wins = {}
    for result in results:
        for snake_number, wins in result.items():
            if snake_number not in total_wins:
                total_wins[snake_number] = 0
            total_wins[snake_number] += wins

    return total_wins

if __name__ == "__main__":
    num_simulations = 10  # Set the number of simulations you want to run
    results = run_parallel_simulations(num_simulations)
    print(f"Results after {num_simulations} simulations:")
    for snake_number, wins in results.items():
        print(f"Snake {snake_number} won {wins} times")