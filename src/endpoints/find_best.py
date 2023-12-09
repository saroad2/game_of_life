import tqdm

from boards_generation import BoardsGeneration
from constants import N, EPOCHS
from offspring_type import OffspringType

if __name__ == '__main__':
    boards_generation = BoardsGeneration.build(n=N, boards_num=1_000)
    print("Warmup...")
    for board in tqdm.tqdm(boards_generation):
        board.calculate_score()
    print("Ready!")
    for i in range(1, EPOCHS + 1):
        boards_generation, offspring_types_dict = boards_generation.build_next_generation(
            crossover_chance=0.06,
            mutation_chance=0.04,
        )
        print(
            f"{i}) "
            f"P: {offspring_types_dict[OffspringType.PICK]}, "
            f"C: {offspring_types_dict[OffspringType.CROSSOVER]}, "
            f"M: {offspring_types_dict[OffspringType.MUTATE]}, "
            f"Mean score={boards_generation.mean_score:.2f}, "
            f"Best score={boards_generation.best_score:.2f}"
        )
