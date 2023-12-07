from board import Board
from constants import MAX_GENERATIONS

if __name__ == '__main__':
    board = Board.random(20)
    print(f"{board.score=}")
    for _ in range(MAX_GENERATIONS):
        print(f"{len(board.live_cells)=}")
        board = board.next_generation()
