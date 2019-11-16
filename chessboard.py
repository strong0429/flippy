#--coding:utf-8--
#定义所需的类
import pygame
import random

LINE_COLOR = (200, 200, 200)
TILE_COLOR = {'W': (255, 255, 255), 'B': (60, 60, 60)}

# 棋盘类：Chessboard
class Chessboard():
    # tiles = {'H': }
    def __init__(self, wnd, size=50, rows=8, cols=8):
        self.main_wnd = wnd        # 游戏主窗口
        self.cell_size = size      # 棋盘格的大小
        self.cell_rows = rows      # 棋盘格的行数
        self.cell_cols = cols      # 棋盘格的列数
        self.r_tile = size//2 - 4  # 棋子半径

        # 记录棋盘格状态：'W': 白方，'B'：黑方，'N': 未落子
        self.cells = [[],[],] 
        # 记录双方当前有效的落子位置
        self.valid_cells = {'W':[()], 'B':[()]}
        # 记录待翻转棋子列表，元素为棋盘行列元组（row，col)   
        self.tiles_to_flip = [(),]
        # 棋子在棋盘上的八个移动方向步长
        self.dir_step = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

        self.init_cells()

        # Rect，记录棋盘的大小及在主窗口的位置
        self.rect = pygame.Rect(0, 0, \
            self.cell_size * self.cell_cols + 1, \
            self.cell_size * self.cell_rows + 1)
        self.rect.center = self.main_wnd.get_rect().center

        # 创建棋盘画布，绘制棋盘背景、网格、棋子
        self.surface = pygame.Surface(self.rect.size)
        # 加载棋盘背景图
        self.bg_img = pygame.image.load('board.jpg')
        self.bg_img = pygame.transform.smoothscale( \
            self.bg_img, (self.rect.w, self.rect.h))
        # 直接在背景图上画棋盘网格线：水平线
        for row in range(self.cell_rows + 1):
            startx = 0
            starty = row * self.cell_size
            endx = self.cell_size * self.cell_cols
            endy = starty
            pygame.draw.line(self.bg_img, LINE_COLOR, \
                (startx, starty), (endx, endy))
        # 画棋盘垂直线
        for col in range(self.cell_cols + 1):
            starty = 0
            startx = col * self.cell_size
            endy = self.cell_size * self.cell_rows
            endx = startx
            pygame.draw.line(self.bg_img, LINE_COLOR, \
                (startx, starty), (endx, endy))

    # 初始化棋盘格
    def init_cells(self):
        self.tiles_to_flip.clear()
        # self.valid_cells.clear()
        self.cells.clear()

        # 创建并初始化棋盘格
        for _ in range(self.cell_rows):
            self.cells.append(['N'] * self.cell_cols)
        # self.cells = [['N'] * self.cell_cols for _ in range(self.cell_rows)]
        startx = self.cell_cols // 2 - 1
        starty = self.cell_rows // 2 - 1
        self.cells[startx][starty] = 'W'
        self.cells[startx][starty + 1] = 'B'
        self.cells[startx + 1][starty] = 'B'
        self.cells[startx + 1][starty + 1] = 'W'

        self.get_valid_cells('W')
        self.get_valid_cells('B')
        
    def draw_tile(self, row, col):
        # 确定棋子圆心坐标
        circlex = self.cell_size * col + self.cell_size // 2
        circley = self.cell_size * row + self.cell_size // 2
        # 在棋盘画布上画棋子：黑/白实心圆
        tile = self.cells[row][col]
        pygame.draw.circle(self.surface, TILE_COLOR[tile], 
            (circlex, circley), self.r_tile)

    def draw_board(self):
        # 用黑色覆盖棋盘画布
        self.surface.fill((0, 0, 0))
        # 绘制背景和网格线
        self.surface.blit(self.bg_img, (0, 0))
        # 绘制棋子
        for row, cells in enumerate(self.cells):
            for col, cell in enumerate(cells):
                if cell == 'N':
                    continue
                self.draw_tile(row, col)
        # 棋盘画布绘制到主窗口
        self.main_wnd.blit(self.surface, self.rect)
        # 翻转棋子（动画效果）
        if self.tiles_to_flip:
            for _ in range(4):
                pygame.display.update()
                pygame.time.wait(150)
                for row, col in self.tiles_to_flip:
                    self.cells[row][col] = ('W', 'B')[self.cells[row][col]=='W']
                    self.draw_tile(row, col)
                self.main_wnd.blit(self.surface, self.rect)
            self.tiles_to_flip = []

    def get_tiles_to_flip(self, row, col, color):
        tiles = []
        for x_step, y_step in self.dir_step:
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
                if self.cells[nxt_row][nxt_col] == color:
                    tiles += tmp_tiles
                    break
                # 对方棋子，添加到待确认列表
                tmp_tiles.append((nxt_row, nxt_col))
        return tiles

    # 判断当前位置是否可以放置tile棋子
    def is_valid(self, row, col, tile):
        valid = False
        for x_step, y_step in self.dir_step:
            nxt_row, nxt_col = row, col
            while True:
                # 当前方向移动一步
                nxt_row += y_step
                nxt_col += x_step
                # 超出棋盘或空位，未封闭，放弃待确认棋子
                if not (0 <= nxt_row < self.cell_rows and \
                    0 <= nxt_col < self.cell_cols) or \
                    self.cells[nxt_row][nxt_col] == 'N':
                    valid = False
                    break
                # 己方棋子，封闭，添加到待翻转棋子列表
                if self.cells[nxt_row][nxt_col] == tile:
                    break
                # 对方棋子，valid置未True
                valid = True
            if valid == True:
                break
        return valid

    # player走棋
    def set_tile(self, x, y, tile):
        # 去除左边和顶部空白后，转换为棋盘的行、列   
        row = (y - self.rect.y) // self.cell_size
        col = (x - self.rect.x) // self.cell_size
        # 是否有效位置
        if (row, col) not in self.valid_cells[tile]:
            return False
        # 翻转对方棋子
        self.cells[row][col] = tile
        self.tiles_to_flip = self.get_tiles_to_flip(row, col, tile)
        for row, col in self.tiles_to_flip:
            self.cells[row][col] = tile
        return True

    # 获取指定颜色棋子当前所有可落子格子
    def get_valid_cells(self, tile):
        valid_cells = []
        for row in range(self.cell_rows):
            for col in range(self.cell_cols):
                if self.cells[row][col] != 'N':
                    continue
                if self.is_valid(row, col, tile):
                    valid_cells.append((row, col))
        self.valid_cells[tile] = valid_cells
        return valid_cells

    # 计算机走棋
    def set_tile_AI(self, tile):
        # 随机选择一个有效位置
        row, col = random.choice(self.valid_cells[tile])
        self.cells[row][col] = tile
        # 翻转对方棋子
        self.tiles_to_flip = self.get_tiles_to_flip(row, col, tile)
        for row, col in self.tiles_to_flip:
            self.cells[row][col] = tile

    # 检查是否还有可以落子的格子，若无则比赛结束
    def check_valid(self):
        if self.valid_cells['W'] or self.valid_cells['B']:
            return True
        return False

    # 以字典方式返回黑、白棋子的数量
    def tile_count(self):
        w_cell, b_cell = 0, 0
        for cell_row in self.cells:
            w_cell += cell_row.count('W')
            b_cell += cell_row.count('B')
        return {'W': w_cell, 'B': b_cell}

    # 走子提示
    def move_hint(self, tile, host):
        r = (self.main_wnd.get_rect().w - self.rect.w) // 8
        if host:
            x = r * 2
        else:
            x = r * 2 + self.rect.right 
        y = self.rect.centery
        pygame.draw.circle(self.main_wnd, TILE_COLOR[tile], (x, y), r)

