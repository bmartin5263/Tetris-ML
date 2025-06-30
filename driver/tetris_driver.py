import pygame

from game.tetris import *


def main():
    COLUMNS, ROWS = 10, 24

    tetris = Tetris(ROWS, COLUMNS)
    # tetris.board = [
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.Empty for _ in range(COLUMNS)],
    #     [Block.I for _ in range(COLUMNS-1)] + [Block.Empty],
    #     [Block.J for _ in range(COLUMNS-1)] + [Block.Empty],
    #     [Block.Z for _ in range(COLUMNS-1)] + [Block.Empty],
    #     [Block.S for _ in range(COLUMNS-1)] + [Block.Empty]
    # ]
    # tetris.currentPiece = Pieces.I_1
    # tetris._placePiece(tetris.currentPiece, tetris.position)
    pygame.init()

    font = pygame.font.Font(None, 20)

    # Grid dimensions
    CELL_SIZE = 30
    WINDOW_WIDTH = COLUMNS * CELL_SIZE
    WINDOW_HEIGHT = ROWS * CELL_SIZE

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
                    tetris.movePiece(Point(-1, 0))
                elif event.key == pygame.K_RIGHT:
                    tetris.movePiece(Point(1, 0))
                elif event.key == pygame.K_DOWN:
                    tetris.movePiece(Point(0, 1))
                    lastDropAt = now
                elif event.key == pygame.K_d:
                    tetris.drop()
                    lastDropAt = now
                elif event.key == pygame.K_SPACE:
                    tetris.rotateClockwise()
                elif event.key == pygame.K_COMMA:
                    tetris.rotateCounterClockwise()
                elif event.key == pygame.K_PERIOD:
                    tetris.rotateClockwise()
                elif event.key == pygame.K_n:
                    tetris.newGame()
                    lastDropAt = now

        if (now - lastDropAt) > 2000:
            tetris.movePiece(Point(0, 1))
            lastDropAt = now

        # Draw grid
        for row in range(ROWS):
            for col in range(COLUMNS):
                block = tetris.board[row][col]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_MAP[block], rect)

        score = font.render(f"Score: {tetris.score}, Rows: {tetris.rowsCleared}", True, (255, 255, 255))
        pieces = font.render(f"Next: {tetris.nextPiece}, Current: {tetris.currentPiece}", True, (255, 255, 255))
        combos = font.render(f"Singles: {tetris.combos[0]}, Doubles: {tetris.combos[1]}, Triples: {tetris.combos[2]}, Tetrises: {tetris.combos[3]}", True, (255, 255, 255))
        screen.blit(score, (0, 0))
        screen.blit(pieces, (0, 20))
        screen.blit(combos, (0, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()