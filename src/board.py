from dataclasses import dataclass, field


@dataclass
class Board:
    live_cells: set[tuple[int, int]] = field(default_factory=set)

    def reset(self):
        self.live_cells.clear()

    def add_cell(self, x: int, y: int):
        self.live_cells.add((x, y))

    def kill_cell(self, x: int, y: int):
        if self.is_alive(x, y):
            self.live_cells.remove((x, y))

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

    def next_generation(self) -> "Board":
        candidates = set(self.live_cells)
        for x, y in self.live_cells:
            candidates.update(self.get_neighbors(x, y))
        board = Board()
        for x, y in candidates:
            if self.will_survive(x, y):
                board.add_cell(x, y)
        return board

    def live_neighbors_count(self, x: int, y: int) -> int:
        return len(
            [
                neighbor
                for neighbor in self.get_neighbors(x, y)
                if self.is_alive(*neighbor)
            ]
        )

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
