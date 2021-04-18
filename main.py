import pygame
import numpy

pygame.init()
pygame.font.init()

WIDTH = HEIGHT = 900
N = M = 9
SQUARE_SIZE = WIDTH // N
BLACK = (0, 0, 0)
RED = (100, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 128)
BLUE_2 = (0, 0, 255)
FPS = 60


def valid_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num = board[i][j]
                if not possible(i, j, num, board):
                    print(i, j, board[i][j])
                    board[i][j] = num
                    return False
                board[i][j] = num
    return True


def possible(n, m, num, array):
    array[n][m] = 0
    for i in range(9):
        if array[n][i] == num:
            return False
        if array[i][m] == num:
            return False
    m0 = (m // 3) * 3
    n0 = (n // 3) * 3
    for j in range(3):
        for i in range(3):
            if array[n0 + j][m0 + i] == num:
                return False
    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j
    return None


def solver(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if possible(row, col, i, bo):
            bo[row][col] = i

            draw_numbers(bo, None, None)
            pygame.display.update()
            if solver(bo):
                return True
            bo[row][col] = 0
    return False


def color_case(win, n, m):
    pygame.draw.rect(win, RED, (m * SQUARE_SIZE, n * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_numbers(array, i, j):
    draw_board(WIN)

    if i is not None:
        color_case(WIN, i, j)

    for n in range(0, 9):
        for m in range(0, 9):
            if array[n][m] != 0:
                x = SQUARE_SIZE * m + (SQUARE_SIZE // 2) - 15
                y = SQUARE_SIZE * n + (SQUARE_SIZE // 2) - 15
                text_surface = base_font.render(str(int(array[n][m])), True, BLUE_2)
                WIN.blit(text_surface, (x, y))


def mouse_position(pos):
    x, y = pos
    m = x // SQUARE_SIZE
    n = y // SQUARE_SIZE
    return n, m


def draw_board(win):
    win.fill(WHITE)
    for i in range(1, 9):
        pygame.draw.line(win, BLUE, [(i * WIDTH) / 9, 0], [(i * WIDTH) / 9, HEIGHT], 2)
        pygame.draw.line(win, BLUE, [0, (i * HEIGHT) / 9], [WIDTH, (i * HEIGHT) / 9], 2)
    for i in range(1, 3):
        pygame.draw.line(win, BLUE_2, [(i * WIDTH) / 3, 0], [(i * WIDTH) / 3, HEIGHT], 4)
        pygame.draw.line(win, BLUE_2, [0, (i * HEIGHT) / 3], [WIDTH, (i * HEIGHT) / 3], 4)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')
base_font = pygame.font.Font('freesansbold.ttf', 50)


def main():
    status_game, quit_game = True, False
    choose_case = False
    clock = pygame.time.Clock()
    table = numpy.zeros((9, 9), dtype=int)
    n = m = None

    while status_game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status_game = False
                quit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                n, m = mouse_position(pos)
                choose_case = True

            if event.type == pygame.KEYDOWN and choose_case:
                if event.key == pygame.K_1:
                    table[n][m] = 1
                elif event.key == pygame.K_2:
                    table[n][m] = 2
                elif event.key == pygame.K_3:
                    table[n][m] = 3
                elif event.key == pygame.K_4:
                    table[n][m] = 4
                elif event.key == pygame.K_5:
                    table[n][m] = 5
                elif event.key == pygame.K_6:
                    table[n][m] = 6
                elif event.key == pygame.K_7:
                    table[n][m] = 7
                elif event.key == pygame.K_8:
                    table[n][m] = 8
                elif event.key == pygame.K_9:
                    table[n][m] = 9

                choose_case = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not valid_sudoku(table):
                    print('Error')
                    continue
                status_game = False
                solver(table)

        draw_numbers(table, n, m)
        pygame.display.update()

    while not status_game and not quit_game:
        draw_numbers(table, None, None)
        pygame.display.update()
        for e1 in pygame.event.get():
            if e1.type == pygame.QUIT:
                status_game = True


main()
