from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from constants import MAX_GENERATIONS, GENERATION_WEIGHT_DECAY


@dataclass
class Board:
    live_cells: set[tuple[int, int]] = field(default_factory=set)
    _cache_next: Optional["Board"] = field(default=None)
    _cache_score: Optional[float] = field(default=None)

    @classmethod
    def random(cls, n: int) -> "Board":
        board = Board()
        for i in range(n):
            for j in range(n):
                if np.random.randint(2) == 1:
                    board.add_cell(i, j)
        return board

    @property
    def score(self) -> float:
        if self._cache_score is None:
            self.calculate_score()
        return self._cache_score

    @property
    def next_generation(self) -> "Board":
        if self._cache_next is None:
            self.calculate_next_generation()
        return self._cache_next

    def copy(self) -> "Board":
        cache_next = None if self._cache_next is None else self._cache_next.copy()
        return Board(
            live_cells=set(self.live_cells),
            _cache_next=cache_next,
            _cache_score=self._cache_score
        )

    def reset(self):
        self.live_cells.clear()

    def add_cell(self, x: int, y: int):
        self.live_cells.add((x, y))
        self.clear_cache()

    def kill_cell(self, x: int, y: int):
        if self.is_alive(x, y):
            self.live_cells.remove((x, y))
            self.clear_cache()

    def switch_cell(self, x: int, y: int):
        if self.is_alive(x, y):
            self.kill_cell(x, y)
        else:
            self.add_cell(x, y)

    def is_alive(self, x: int, y: int) -> bool:
        return (x, y) in self.live_cells

    def will_survive(self, x: int, y: int) -> bool:
        live_neighbors_count = self.live_neighbors_count(x, y)
        if live_neighbors_count >= 4:
            return False
        if live_neighbors_count == 3:
            return True
        if live_neighbors_count <= 1:
            return False
        return self.is_alive(x, y)

    def live_neighbors_count(self, x: int, y: int) -> int:
        return len(
            [
                neighbor
                for neighbor in self.get_neighbors(x, y)
                if self.is_alive(*neighbor)
            ]
        )

    def calculate_next_generation(self):
        candidates = set(self.live_cells)
        for x, y in self.live_cells:
            candidates.update(self.get_neighbors(x, y))
        board = Board()
        for x, y in candidates:
            if self.will_survive(x, y):
                board.add_cell(x, y)
        self._cache_next = board

    def calculate_score(self):
        board = self
        cells_count = []
        for _ in range(MAX_GENERATIONS):
            cells_count.append(len(board.live_cells))
            board = board.next_generation

        cells_count = np.array(cells_count)

        weights = np.exp(np.linspace(-1, 1, num=MAX_GENERATIONS)) - 1
        weights /= np.sum(np.fabs(weights))

        self._cache_score = float(np.sum(cells_count * weights))

    def clear_cache(self):
        self._cache_next = None
        self._cache_score = None

    @classmethod
    def get_neighbors(cls, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
