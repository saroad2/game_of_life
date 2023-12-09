import time
from pathlib import Path

import pygame

from game_of_life.board import Board
from game_of_life.colors import WHITE, BLACK
from game_of_life.constants import SCREEN_SIZE, BLOCK_SIZE, N, DELAY_SECONDS

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    SAVED_BOARD_FILE = Path.cwd() / 'best_board.json'
    if SAVED_BOARD_FILE.exists():
        board = Board.from_path(SAVED_BOARD_FILE).move(N // 2, N // 2)
    else:
        board = Board()

    running = True
    play = False
    start_time = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                board.switch_cell(x // BLOCK_SIZE, y // BLOCK_SIZE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play
                if event.key == pygame.K_r:
                    board.reset()
                if event.key == pygame.K_g:
                    board = Board.random(N)
                if event.key == pygame.K_n:
                    board = board.normalize()
                if event.key == pygame.K_LEFT:
                    board = board.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    board = board.move(1, 0)
                if event.key == pygame.K_UP:
                    board = board.move(0, -1)
                if event.key == pygame.K_DOWN:
                    board = board.move(0, 1)
        if play:
            now = time.time()
            if start_time is None or now - start_time > DELAY_SECONDS:
                start_time = now
                board = board.next_generation
        else:
            start_time = None
        screen.fill(WHITE)
        for i in range(N):
            for j in range(N):
                pygame.draw.rect(
                    screen,
                    color=BLACK,
                    rect=(i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    width=(0 if board.is_alive(i, j) else 1)
                )
        pygame.display.flip()
    pygame.quit()
