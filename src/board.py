from dataclasses import dataclass, field


@dataclass
class Board:
    live_cells: set[tuple[int, int]] = field(default_factory=set)

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
