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

    def next_generation(self) -> "BoardsGeneration":
        boards = []
        weights = np.array([board.score for board in self.boards])
        weights /= np.sum(weights)
        for _ in range(len(self)):
            index = np.random.choice(len(self), p=weights)
            board = self.boards[index]
            boards.append(board.copy())
        return BoardsGeneration(boards)

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
