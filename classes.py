# 定义所需的类
import pygame

BLACK = (80, 80, 80)
WHITE = (255, 255, 255)
BOARDLINECOLOR = (0, 0, 0)

# 棋盘类：Chessboard
class Chessboard():

    def __init__(self, size=50, rows=8, cols=8):
        self.cell_size = size     # 棋盘格的大小
        self.cell_rows = rows      # 棋盘格的行数
        self.cell_cols = cols      # 棋盘格的列数

        self.cells = [['N'] * self.cell_cols for _ in range(self.cell_rows)]
        startx = self.cell_cols // 2 - 1
        starty = self.cell_rows // 2 - 1
        self.cells[startx][starty] = 'W'
        self.cells[startx][starty + 1] = 'B'
        self.cells[startx + 1][starty] = 'B'
        self.cells[startx + 1][starty + 1] = 'W'

        self.rect = pygame.Rect(0, 0, \
            self.cell_size * self.cell_cols + 1, \
            self.cell_size * self.cell_rows + 1)
        
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.bg_img = pygame.image.load('flippyboard.png')
        self.bg_img = pygame.transform.smoothscale( \
            self.bg_img, (self.rect.w, self.rect.h))
        
        # 直接在背景图上画棋盘网格线：水平线
        for row in range(self.cell_rows + 1):
            startx = 0
            starty = row * self.cell_size
            endx = self.cell_size * self.cell_cols
            endy = starty
            pygame.draw.line(self.bg_img, BOARDLINECOLOR, \
                (startx, starty), (endx, endy))
        # 画棋盘垂直线
        for col in range(self.cell_cols + 1):
            starty = 0
            startx = col * self.cell_size
            endy = self.cell_size * self.cell_rows
            endx = startx
            pygame.draw.line(self.bg_img, BOARDLINECOLOR, \
                (startx, starty), (endx, endy))

    def draw_cells(self):
        r = self.cell_size // 2 - 3
        for row, cells in enumerate(self.cells):
            for col, cell in enumerate(cells):
                if cell == 'N':
                    continue
                circlex = self.cell_size * col + self.cell_size // 2
                circley = self.cell_size * row + self.cell_size // 2
                if cell == 'W':
                    pygame.draw.circle(self.surface, WHITE, (circlex, circley), r)
                elif cell == 'B':
                    pygame.draw.circle(self.surface, BLACK, (circlex, circley), r)

    def draw_board(self, game_wnd):
        self.surface.fill(BLACK)
        self.surface.blit(self.bg_img, (0, 0))
        self.draw_cells()

        rect = game_wnd.get_rect()
        self.rect.center = rect.center
        game_wnd.blit(self.surface, self.rect)

    