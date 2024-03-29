import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

from game_of_life.constants import MAX_GENERATIONS, SCORE_WEIGHTS


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

    @classmethod
    def from_path(cls, path: Path) -> "Board":
        board = Board()
        with open(path, "r") as fd:
            data = json.load(fd)
        for x, y in data["live_cells"]:
            board.add_cell(x, y)
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

    @property
    def box(self) -> tuple[int, int, int, int]:
        x_values = [x for x, _ in self.live_cells]
        y_values = [y for _, y in self.live_cells]

        min_x, max_x = np.min(x_values), np.max(x_values)
        min_y, max_y = np.min(y_values), np.max(y_values)
        return min_x, min_y, max_x, max_y

    def copy(self) -> "Board":
        cache_next = None if self._cache_next is None else self._cache_next.copy()
        return Board(
            live_cells=set(self.live_cells),
            _cache_next=cache_next,
            _cache_score=self._cache_score
        )

    def move(self, dx: int, dy: int) -> "Board":
        new_cells = {
            (x + dx, y + dy)
            for x, y in self.live_cells
        }
        cache_next = None if self._cache_next is None else self._cache_next.move(dx, dy)
        return Board(
            new_cells,
            _cache_next=cache_next,
            _cache_score=self._cache_score
        )

    def normalize(self) -> "Board":
        min_x, min_y, _, _ = self.box
        return self.move(-min_x, -min_y)

    def flip_xy(self) -> "Board":
        new_cells = {
            (y, x)
            for x, y in self.live_cells
        }
        cache_next = None if self._cache_next is None else self._cache_next.flip_xy()
        return Board(
            new_cells,
            _cache_next=cache_next,
            _cache_score=self._cache_score
        )

    def mirror_x(self) -> "Board":
        new_cells = {
            (-x, y)
            for x, y in self.live_cells
        }
        cache_next = None if self._cache_next is None else self._cache_next.mirror_x()
        return Board(
            new_cells,
            _cache_next=cache_next,
            _cache_score=self._cache_score
        )

    def mirror_y(self) -> "Board":
        new_cells = {
            (x, -y)
            for x, y in self.live_cells
        }
        cache_next = None if self._cache_next is None else self._cache_next.mirror_y()
        return Board(
            new_cells,
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

        self._cache_score = float(np.sum(cells_count * SCORE_WEIGHTS))

    def clear_cache(self):
        self._cache_next = None
        self._cache_score = None

    def export(self, path: Path):
        obj = dict(
            live_cells=[
                (int(x), int(y))
                for x, y in self.live_cells
            ]
        )
        with open(path, "w") as fd:
            json.dump(obj, fd, indent=1)

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
