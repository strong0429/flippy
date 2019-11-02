# Flippy游戏主程序文件

import sys, pygame
from pygame.locals import *

from chessboard import *
from publib import *

FPS = 15    # 每秒刷新屏幕的次数
NETWORK = False # 是否联网
WND_W, WND_H = 640, 480 # 游戏窗口的宽、高

# 游戏主程序入口函数
def main():
    pygame.init()
    # 创建游戏窗口
    game_wnd = pygame.display.set_mode((WND_W, WND_H))
    pygame.display.set_caption('翻转棋')

    # 加载窗口背景图案
    bg_img = pygame.image.load('flippy_bg.png')
    bg_img = pygame.transform.smoothscale(bg_img, (WND_W, WND_H))
    game_wnd.blit(bg_img, (0, 0))
    pygame.display.update()

    # 选择游戏模式

    tiles = ['W', 'B']
    turn = random.choice(tiles)
    player = random.choice(tiles)
    Ai = tiles[player=='W']

    board = Chessboard(game_wnd)

    clock = pygame.time.Clock()
    pygame.event.clear()
    while True:
        if not board.check_valid():
            result = board.tile_count()
            if result[player] > result[Ai]:
                yes = query_box("你赢了！再来一局？", game_wnd, f_size=24)
            elif result[player] < result[Ai]:
                yes = query_box("你输了！再来一局？", game_wnd, f_size=24)
            else:
                yes = query_box("你输了！再来一局？", game_wnd, f_size=24)
            if not yes:
                break
            board.init_cells()

        # 检查QUIT事件
        event = pygame.event.poll()
        if event.type == QUIT:
            if query_box('确认终止比赛吗？', game_wnd, f_color=(160,0,0), f_size=30):
                break

        if turn == player:
            if board.get_valid_cells(player):
                if event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    if board.set_tile(x, y, player):
                        turn = Ai
            else:
                turn = Ai
        else:
            pygame.time.wait(500)
            if board.get_valid_cells(Ai):
                board.set_tile_AI(Ai)
            turn = player
        pygame.event.clear()

        game_wnd.blit(bg_img, (0, 0))
        board.bb_update(player, Ai)
        board.draw_board()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

# 游戏入口
if __name__ == '__main__':
    main()