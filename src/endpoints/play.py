import time

import pygame

from board import Board
from colors import WHITE, BLACK
from constants import SCREEN_SIZE, BLOCK_SIZE, N, DELAY_SECONDS

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

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
