import tqdm

from boards_generation import BoardsGeneration
from constants import N

if __name__ == '__main__':
    boards_generation = BoardsGeneration.build(n=N, boards_num=1_000)
    print("Warmup...")
    for board in tqdm.tqdm(boards_generation):
        board.calculate_score()
    print("Ready!")
    for i in range(1, 101):
        boards_generation = boards_generation.build_next_generation(
            mutation_chance=0.1,
            crossover_chance=0.1,
        )
        print(
            f"{i}) "
            f"Mean score={boards_generation.mean_score:.2f}, "
            f"Best score={boards_generation.best_score:.2f}"
        )
