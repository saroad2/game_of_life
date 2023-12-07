import pygame

from colors import WHITE, BLACK
from constants import SCREEN_SIZE, BLOCK_SIZE, N

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        for i in range(N):
            for j in range(N):
                pygame.draw.rect(
                    screen,
                    color=BLACK,
                    rect=(i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    width=1
                )
        pygame.display.flip()
    pygame.quit()
