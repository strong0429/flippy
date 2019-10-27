# 定义所需的类
import pygame
import random

BLACK = (50, 50, 50)
WHITE = (255, 255, 255)
BOARDLINECOLOR = (0, 0, 0)

# 棋盘类：Chessboard
class Chessboard():

    def __init__(self, wnd, size=50, rows=8, cols=8):
        self.cell_size = size     # 棋盘格的大小
        self.cell_rows = rows      # 棋盘格的行数
        self.cell_cols = cols      # 棋盘格的列数
        self.main_wnd = wnd

        # self.cells = [['N'] * self.cell_cols for _ in range(self.cell_rows)]
        self.cells = []
        for _ in range(self.cell_rows):
            self.cells.append(['N'] * self.cell_cols)
        startx = self.cell_cols // 2 - 1
        starty = self.cell_rows // 2 - 1
        self.cells[startx][starty] = 'W'
        self.cells[startx][starty + 1] = 'B'
        self.cells[startx + 1][starty] = 'B'
        self.cells[startx + 1][starty + 1] = 'W'

        self.rect = pygame.Rect(0, 0, \
            self.cell_size * self.cell_cols + 1, \
            self.cell_size * self.cell_rows + 1)
        self.rect.center = self.main_wnd.get_rect().center
        
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

    def draw_tiles(self):
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

    def draw_board(self):
        self.surface.fill(BLACK)
        self.surface.blit(self.bg_img, (0, 0))
        self.draw_tiles()
        self.main_wnd.blit(self.surface, self.rect)

    def is_valide(self, row, col, tile):
        tiles_to_flip = []
        dir_step = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for x_step, y_step in dir_step:
            nxt_row, nxt_col = row, col
            tmp_tiles = []  # 待确认翻转棋子
            while True:
                # 当前方向移动一步
                nxt_row += y_step
                nxt_col += x_step
                # 超出棋盘或空位，未封闭，放弃待确认棋子
                if not (0 <= nxt_row < self.cell_rows and 0 <= nxt_col < self.cell_cols) or\
                    self.cells[nxt_row][nxt_col] == 'N':
                    break
                # 己方棋子，封闭，添加到待翻转棋子列表
                if self.cells[nxt_row][nxt_col] == tile:
                    tiles_to_flip += tmp_tiles
                    break
                # 对方棋子，添加到待确认列表
                tmp_tiles.append((nxt_row, nxt_col))
        return tiles_to_flip


    def set_tile(self, x, y, tile):
        #判断x，y坐标是否在棋盘内
        if not (self.rect.x < x < self.rect.x + self.rect.w and \
            self.rect.y < y < self.rect.y + self.rect.h):
            return
        # 去除左边和顶部空白    
        cellx = x - self.rect.x
        celly = y - self.rect.y
        # 坐标转换为行、列
        row = celly // self.cell_size
        col = cellx // self.cell_size
        # 是否有效位置
        tiles_to_flip = self.is_valide(row, col, tile)
        if tiles_to_flip:
            self.cells[row][col] = tile
            for row, col in tiles_to_flip:
                self.cells[row][col] = tile


