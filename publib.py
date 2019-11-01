#--coding:utf-8--

import pygame

# 询问框
def query_box(msg, wnd, f_name=None, f_color=None, f_size=None):
    #创建字体
    if f_name is None:
        f_name = 'STZHONGS.ttf'
    if f_color is None:
        f_color = (0, 0, 0)
    if f_size is None:
        f_size = 18
    font = pygame.font.Font(f_name, f_size)
    msg_img = font.render(msg, True, f_color)
    yes_img = font.render(' Yes ', True, f_color, (128, 128, 128))
    no_img = font.render(' No ', True, f_color, (128, 128, 128))
    
    # 创建询问框surface
    yes_rect = msg_img.get_rect()
    box_rect = yes_rect.copy()
    box_rect.w = int(box_rect.w * 1.2) + 10
    box_rect.h = int(box_rect.h * 2.5) + 10
    box_surface = pygame.Surface(box_rect.size)
    
    box_surface.fill((200, 200, 200))
    # 2px边框
    box_rect.x = 1
    box_rect.y = 1
    box_rect.w -= 2
    box_rect.h -= 2
    pygame.draw.rect(box_surface, (128, 128, 128), box_rect, 2)
    box_rect = box_surface.get_rect()
    box_rect.center = wnd.get_rect().center

    # 打印信息文本
    yes_rect.topleft = (5, 5)
    box_surface.blit(msg_img, yes_rect)
    yes_rect.size = yes_img.get_rect().size
    yes_rect.x = (box_rect.w//2 - yes_rect.w) // 2
    yes_rect.y = (yes_rect.bottom + yes_rect.h//2)
    box_surface.blit(yes_img, yes_rect)
    no_rect = no_img.get_rect()
    no_rect.x = yes_rect.x + (box_rect.w // 2)
    no_rect.y = yes_rect.y 
    box_surface.blit(no_img, no_rect)

    # 转换为父窗口的坐标
    no_rect.x += box_rect.x
    no_rect.y += box_rect.y
    yes_rect.x += box_rect.x
    yes_rect.y += box_rect.y

    # 获取用户输入
    pygame.event.clear()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            if yes_rect.collidepoint(event.pos):
                return True
            elif no_rect.collidepoint(event.pos):
                return False
        wnd.blit(box_surface, box_rect)
        pygame.display.flip()
        pygame.time.wait(50)








