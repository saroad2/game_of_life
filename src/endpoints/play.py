import pygame

from board import Board
from colors import WHITE, BLACK
from constants import SCREEN_SIZE, BLOCK_SIZE, N

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                board.switch_cell(x // BLOCK_SIZE, y // BLOCK_SIZE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board = board.next_generation()
                if event.key == pygame.K_r:
                    board.reset()
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
