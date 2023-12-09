from dataclasses import dataclass

import numpy as np
import tqdm

from game_of_life.board import Board
from game_of_life.constants import N
from game_of_life.offspring_type import OffspringType


@dataclass()
class BoardsGeneration:
    boards: list[Board]

    def __len__(self):
        return len(self.boards)

    def __iter__(self):
        return iter(self.boards)

    def build_next_generation(
        self,
        mutation_chance: float,
        crossover_chance: float,
        random_chance: float,
    ) -> tuple["BoardsGeneration", dict[OffspringType, int]]:
        boards = []
        types_dict = dict.fromkeys(OffspringType, 0)
        for _ in tqdm.trange(len(self)):
            board, offspring_type = self.get_board(
                mutation_chance=mutation_chance,
                crossover_chance=crossover_chance,
                random_chance=random_chance,
            )
            types_dict[offspring_type] += 1
            boards.append(board)
        return BoardsGeneration(boards), types_dict

    def get_board(
        self,
        mutation_chance: float,
        crossover_chance: float,
        random_chance: float,
    ) -> tuple[Board, OffspringType]:
        effect = np.random.uniform(0, 1)
        if effect < random_chance:
            return Board.random(N), OffspringType.RANDOM
        effect -= random_chance
        board = self.pick()
        if effect < mutation_chance:
            return self.mutate(board), OffspringType.MUTATE
        effect -= mutation_chance
        if effect < crossover_chance:
            board2 = self.pick()
            return self.crossover(board, board2), OffspringType.CROSSOVER
        return board, OffspringType.PICK

    def pick(self):
        weights = np.array(self.scores)
        weights -= np.min(weights)
        weights /= np.sum(weights)
        index = np.random.choice(len(self), p=weights)
        return self.boards[index].copy()

    @classmethod
    def mutate(cls, board: Board) -> Board:
        _, _, max_x, max_y = board.box
        new_board = board.copy()
        i = np.random.choice(max_x + 1)
        j = np.random.choice(max_y + 1)
        new_board.switch_cell(i, j)
        new_board.calculate_score()
        return new_board.normalize()

    @classmethod
    def crossover(cls, board1: Board, board2: Board) -> Board:
        new_board = Board()
        candidates = set(board1.live_cells)
        candidates.update(board2.live_cells)
        for x, y in candidates:
            if cls.survives_crossover(board1, board2, x, y):
                new_board.add_cell(x, y)
        new_board.calculate_score()
        return new_board.normalize()

    @classmethod
    def survives_crossover(cls, board1: Board, board2: Board, x: int, y: int) -> bool:
        if board1.is_alive(x, y) and board2.is_alive(x, y):
            return True
        if not board1.is_alive(x, y) and not board2.is_alive(x, y):
            return False
        return np.random.randint(2) == 1

    @classmethod
    def build(cls, n: int, boards_num: int) -> "BoardsGeneration":
        return BoardsGeneration(
            [
                Board.random(n).normalize()
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
