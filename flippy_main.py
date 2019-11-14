# Flippy游戏主程序文件
import sys, pygame
from pygame.locals import *
from chessboard import *
from publib import *

FPS = 15    # 每秒刷新屏幕的次数
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
    # 显示背景
    game_wnd.blit(bg_img, (0, 0))
    # 创建网络
    network = Network()
    network.start()
    # 创建棋盘
    board = Chessboard(game_wnd)
    host, guest, turn = ('', '', '')

    clock = pygame.time.Clock()
    pygame.event.clear()    # 清空消息队列
    while True:
        pygame.display.update()
        clock.tick(FPS)

        # 检查QUIT事件
        event = pygame.event.poll()
        if event.type == QUIT:
            if query_box('确认终止比赛吗？', game_wnd, f_color=(160,0,0), f_size=24):
                break
        # 获取网络状态
        stat = network.get_stat()
        if stat == 'connecting':
            msg_box('等待网络连接...', game_wnd)
            continue
        if stat == 'close' or stat == 'noreply':
            msg_box('对方退出比赛，游戏结束！', game_wnd)
            continue
        # 确定主、客方及轮次
        if not (host and guest and turn) and network.host:
            host, guest, turn = 'W', 'B', 'B'
        elif not (host and guest and turn):
            host, guest, turn = 'B', 'W', 'B'
        
        if turn == host:    #主方下子
            if board.get_valid_cells(host):
                if event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    if board.set_tile(x, y, host):
                        network.send_msg('move,%04d,%04d' % (x, y))
                        turn = guest
            else:
                network.send_msg('move,none')
                turn = guest
        else:   # 客方下子
            msg = network.get_msg()
            if msg and 'move' in msg:
                turn = host
                board.get_valid_cells(guest)
                if 'none' not in msg:
                    x = int(msg[5:9:])
                    y = int(msg[10:14:])
                    board.set_tile(x, y, guest)
        pygame.event.clear()

        game_wnd.blit(bg_img, (0, 0))
        board.draw_board()
        
        # 判断比赛是否结束
        if board.check_valid():
            tile, ishost = (host, True) if turn == host else (guest, False)
            board.move_hint(tile, ishost)
        else:
            result = board.tile_count()
            board.move_hint(host, True)
            msg_box('比赛结束！主方%d子，客方%d子。'%(result[host], result[guest]), game_wnd)

    network.close()
    pygame.quit()

# 游戏入口
if __name__ == '__main__':
    main()
