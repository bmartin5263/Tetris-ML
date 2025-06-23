import pygame

from game.tetris import *


def main():
    GRID_WIDTH, GRID_HEIGHT = 10, 10
    E = Block.Empty

    tetris = Tetris(GRID_HEIGHT, GRID_WIDTH)
    tetris.board = [
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.Empty for _ in range(GRID_WIDTH)],
        [Block.I for _ in range(GRID_WIDTH-1)] + [Block.Empty],
        [Block.J for _ in range(GRID_WIDTH-1)] + [Block.Empty],
        [Block.Z for _ in range(GRID_WIDTH-1)] + [Block.Empty],
        [Block.S for _ in range(GRID_WIDTH-1)] + [Block.Empty]
    ]
    tetris.currentPiece = Pieces.I_1
    tetris._placePiece(tetris.currentPiece, tetris.position)
    pygame.init()

    # Grid dimensions
    CELL_SIZE = 30
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

    COLOR_MAP = {
        Block.Empty: (0, 0, 0),
        Block.I: (255, 0, 0),
        Block.J: (255, 100, 0),
        Block.L: (0, 0, 255),
        Block.S: (0, 255, 0),
        Block.Z: (255, 0, 255),
        Block.T: (0, 255, 255),
        Block.O: (255, 255, 0),
    }

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Main loop
    running = True
    clock = pygame.time.Clock()
    lastDropAt = clock.get_time()

    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.makeAction(Action.MOVE_LEFT)
                elif event.key == pygame.K_RIGHT:
                    tetris.makeAction(Action.MOVE_RIGHT)
                elif event.key == pygame.K_DOWN:
                    tetris.makeAction(Action.MOVE_DOWN)
                    lastDropAt = now
                elif event.key == pygame.K_d:
                    tetris.makeAction(Action.DROP)
                    lastDropAt = now
                elif event.key == pygame.K_SPACE:
                    tetris.makeAction(Action.ROTATE_CW)
                elif event.key == pygame.K_COMMA:
                    tetris.makeAction(Action.ROTATE_CCW)
                elif event.key == pygame.K_PERIOD:
                    tetris.makeAction(Action.ROTATE_CW)
                elif event.key == pygame.K_n:
                    tetris.newGame()
                    lastDropAt = now

        if (now - lastDropAt) > 2000:
            tetris.makeAction(Action.MOVE_DOWN)
            lastDropAt = now

        # Draw grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                block = tetris.board[row][col]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_MAP[block], rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()