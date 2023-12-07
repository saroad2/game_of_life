from dataclasses import dataclass

import numpy as np

from board import Board


@dataclass()
class BoardsGeneration:
    boards: list[Board]

    def __len__(self):
        return len(self.boards)

    def __iter__(self):
        return iter(self.boards)

    def next_generation(self, mutation_chance: float = 0.0) -> "BoardsGeneration":
        boards = []
        for _ in range(len(self)):
            board = self.pick()
            if np.random.uniform(0, 1) < mutation_chance:
                board = board.next_generation
            boards.append(board)
        return BoardsGeneration(boards)

    def pick(self):
        weights = np.array(self.scores)
        weights /= np.sum(weights)
        index = np.random.choice(len(self), p=weights)
        return self.boards[index].copy()

    @classmethod
    def build(cls, n: int, boards_num: int) -> "BoardsGeneration":
        return BoardsGeneration(
            [
                Board.random(n)
                for _ in range(boards_num)
            ]
        )

    @property
    def mean_score(self) -> float:
        return np.mean(self.scores)

    @property
    def best_score(self) -> float:
        return np.max(self.scores)

    @property
    def scores(self) -> list[float]:
        return [board.score for board in self.boards]
