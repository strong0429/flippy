#--coding:utf-8--

import random, time, threading
import pygame
import socket

# 定义网络类，
class Network():
    def __init__(self):
        self.port = 0
        self.sock = None
        self.remote = None
        self.recv_msg = {}
        self.receiver = None
        self.running = False

    # 建立网络连接
    def init(self, port=9091):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.settimeout(0.1)
        #self.sock.setblocking(False)
        #self.sock.bind(('', self.port))

        self.running = True
        self.receiver = threading.Thread(target=self.recv_thread)
        self.receiver.start()

    def recv_thread(self):
        self.recv_msg['sta'] = ('err', '未连接远程主机')

        self.sock.settimeout(1)
        msg = '天王盖地虎'
        for _ in range(random.randint(1, 10)):
            self.sock.sendto(msg.encode('utf-8'), ('<broadcast>', self.port))
            try:
                data, address = self.sock.recvfrom(1024)
                print(data.decode('utf-8'))
                if data.decode('utf-8') == '宝塔镇河妖':
                    print('connect:', address)
                    self.remote = address
                    break
            except Exception as e: #BlockingIOError:
                print(e, type(e))
                continue
        
        if not self.remote:
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #self.sock.settimeout(None)  # 阻塞
            self.sock.bind(('', self.port))
            while True:
                data, address = self.sock.recvfrom(1024)
                print(data.decode('utf-8'))
                if data.decode('utf-8') == '天王盖地虎':
                    print('be connect:', address)
                    data = '宝塔镇河妖'.encode('utf-8')
                    self.sock.sendto(data, address)
                    self.remote = address
                    break
        self.recv_msg['sta'] = ('ok', self.remote)

        self.sock.settimeout(3.0)
        self.sock.connect(self.remote)
        while self.running:
            try:
                data = self.sock.recv(1024)
                print(data.decode('utf-8'))
                if data.decode('utf-8') == 'hello?':
                    self.recv_msg['sta'] = ('ok', 'nothing')
                    data = 'fine!'.encode('utf-8')
                    self.sock.send(data)
            except Exception as e:
                print(e, type(e))
                data = 'hello?'.encode('utf-8')
                self.sock.send(data)
                try:
                    data = self.sock.recv(1024)
                    if data.decode('utf-8') != 'fine!':
                        self.recv_msg['sta'] = ('err', '远程主机无应答')
                except:
                    self.recv_msg['sta'] = ('err', '远程主机无应答')
                continue
            print(self.recv_msg['sta'])
            self.recv_msg['rec'] = data.decode('utf-8')
        
        self.remote = None
        self.sock.close()
                        



    

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








