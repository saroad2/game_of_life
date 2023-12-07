from dataclasses import dataclass

import numpy as np

from board import Board


@dataclass()
class BoardsGeneration:
    boards: list[Board]

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
        return np.mean([board.score for board in self.boards])
