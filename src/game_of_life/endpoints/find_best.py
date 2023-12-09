from pathlib import Path

import tqdm

from game_of_life.boards_generation import BoardsGeneration
from game_of_life.constants import N, EPOCHS
from game_of_life.offspring_type import OffspringType

if __name__ == '__main__':
    boards_generation = BoardsGeneration.build(n=N, boards_num=1_000)
    print("Warmup...")
    for board in tqdm.tqdm(boards_generation):
        board.calculate_score()
    print("Ready!")
    for i in range(1, EPOCHS + 1):
        boards_generation, offspring_types_dict = boards_generation.build_next_generation(
            crossover_chance=0.06,
            mutation_chance=0.03,
            random_chance=0.01,
        )
        print(
            f"{i}) "
            f"P: {offspring_types_dict[OffspringType.PICK]}, "
            f"C: {offspring_types_dict[OffspringType.CROSSOVER]}, "
            f"M: {offspring_types_dict[OffspringType.MUTATE]}, "
            f"R: {offspring_types_dict[OffspringType.RANDOM]}, "
            f"Mean score={boards_generation.mean_score:.2f}, "
            f"Best score={boards_generation.best_score:.2f}"
        )
    boards_generation.best_board.export(Path.cwd() / "best_board.json")
