import random
import numpy as np
import numpy.typing as npt
from ais.ekans.state import State, search_for_move
from ais.ai import EkansAI
from game_objects.snake import Snake, Grid
from constants import GRID_HEIGHT, GRID_WIDTH


def random_weights() -> npt.NDArray: ...


def evolve_weights(
    initial_weights: npt.NDArray, population_size: int, num_generations: int
) -> npt.NDArray:
    population = [random_weights() for i in range(population_size)]
    for generation in range(num_generations):
        new_generation = generate_new_population(population)
        scores = run_tournaments(new_generation, num_rounds=100)

        scored_pop = sorted(list(zip(new_generation, scores)), key=lambda x: -x[1])

        population = [p for p, _ in scored_pop[:population_size]]

        np.save(f"./weights/best_{generation}.npy", population[0])

    return population[0]


def generate_new_population(population: list[npt.NDArray]) -> list[npt.NDArray]:
    new_population = [p for p in population]
    n = len(population)
    boss = population[0]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            new_population.append(boss + mutation(population[i] - population[j]))

    return new_population


def mutation(arr):
    return arr + np.random.normal(loc=1, scale=0.1, size=arr.shape[0])


def run_tournaments(population, num_rounds):
    n = len(population)
    scores = np.zeros(n)
    for i in range(num_rounds):
        order = np.random.permutation(n)
        for i in range(0, n, 4):
            results = play_game(order[i], order[i + 1], order[i + 2], order[i + 3])
            for place, player in enumerate(results):
                scores[player] += (4 - place) ** 2

    return scores


def play_game(player1, player2, player3, player4):
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    new_grid = grid.get_grid()
    snakes, ais = get_snakes(grid)

    ais[0].weights = player1
    ais[1].weights = player2
    ais[2].weights = player3
    ais[3].weights = player4

    order = [0, 0, 0, 0]
    current_order = 4
    snakes_alive = [snake for snake in snakes if snake.alive]

    while len(snakes_alive) > 1:
        for snake in snakes:
            if snake.alive:
                snake.special_move("turbo")
                snake.move()
                if grid.check_collision(snake):
                    snake.alive = False
                    order[snake.number] = current_order
                    current_order -= 1
                snake.grid.update_snake_position(snake)

        # Draw everything
        new_grid = grid.get_grid()
        for AI, snake in zip(ais, snakes):
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

    return order


def get_snakes(grid):
    snakes = [
        Snake(
            initial_position=get_random_start(grid),
            direction="RIGHT",
            color=(0, 255, 0),
            grid=grid,
            number=0,
            name="preskok",
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="LEFT",
            color=(255, 0, 0),
            grid=grid,
            number=1,
            name="sonce",
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="UP",
            color=(0, 0, 255),
            grid=grid,
            number=2,
            name="delo",
        ),
        Snake(
            initial_position=get_random_start(grid),
            direction="LEFT",
            color=(255, 0, 255),
            grid=grid,
            number=3,
            name="tax-fin-lex",
        ),
    ]

    AIs = [EkansAI(), EkansAI(), EkansAI(), EkansAI()]
    return snakes, AIs


def get_random_start(grid):
    return random.choice(range(2, len(grid.grid[0]) - 2)), random.choice(
        range(2, len(grid.grid) - 2)
    )
