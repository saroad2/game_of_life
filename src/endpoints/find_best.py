from boards_generation import BoardsGeneration

if __name__ == '__main__':
    boards_generation = BoardsGeneration.build(n=20, boards_num=100)
    print(f"{boards_generation.mean_score=}")
