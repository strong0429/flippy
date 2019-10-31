# Flippy游戏主程序文件

import sys, pygame
import easygui as gui
from pygame.locals import *

from classes import *

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
    bg_img = pygame.image.load('board.jpg')
    bg_img = pygame.transform.smoothscale(bg_img, (WND_W, WND_H))
    game_wnd.blit(bg_img, (0, 0))
    pygame.display.update()

    # 选择游戏模式
    modes = ['挑战AI（单机模式）', '双人博弈（联网模式）']
    game_mode = gui.choicebox('请选择你喜欢的游戏模式？', '游戏模式', modes)
    if game_mode == modes[1]:
        NETWORK = True
    else:
        NETWORK = False

    tiles = ['W', 'B']
    turn = random.choice(tiles)
    player = random.choice(tiles)
    Ai = tiles[player=='W']
    print(turn, player, Ai)

    board = Chessboard(game_wnd)

    clock = pygame.time.Clock()
    pygame.event.clear()
    while board.check_valid():
        # 检查QUIT事件
        event = pygame.event.poll()
        if event.type == QUIT:
            return

        if turn == player:
            if board.get_valid_cells(player):
                if event.type == MOUSEBUTTONUP:
                    if board.set_tile(event.pos[0], event.pos[1], player):
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
        board.bb_update(player)
        board.draw_board()
        pygame.display.update()
        clock.tick(FPS)

    tile_count = board.tile_count()
    print(tile_count)
    if tile_count[player] > tile_count[Ai]:
        gui.msgbox('比赛结束, 你赢了！')
    elif tile_count[player] == tile_count[Ai]:
        gui.msgbox('比赛结束, 难分伯仲！')
    else:
        gui.msgbox('比赛结束, 你输了！')

# 游戏入口
if __name__ == '__main__':
    main()