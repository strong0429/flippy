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
        self.state = None
        self.inf_msg = {}
        self.rep_msg = {}
        self.receiver = None
        self.running = False
        self.host = True

        self.msg_id = 0
        self.tmp_id = ['']*10

    # 建立网络连接
    def start(self, port=9091):
        self.port = port
        self.receiver = threading.Thread(target=self.recv_thread, daemon=True)
        self.receiver.start()
        self.running = True

        self.state = 'connecting'
        self.timeout = time.time()

    def recv_thread(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.setblocking(False)
        self.sock.settimeout(0.5)

        msg = 'inf:0:天王盖地虎'
        for _ in range(random.randint(1, 5)):
            self.sock.sendto(msg.encode('utf-8'), ('<broadcast>', self.port))
            try:
                data, address = self.sock.recvfrom(1024)
                if data.decode('utf-8') == ('rep:0:宝塔镇河妖'):
                    self.remote = address
                    self.host = False
                    break
            except: #BlockingIOError:
                continue

        if not self.remote:
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(('', self.port))
            self.sock.settimeout(None)
            while True:
                data, address = self.sock.recvfrom(1024)
                data = data.decode('utf-8')
                if data == 'inf:0:天王盖地虎':
                    data = 'rep:0:宝塔镇河妖'.encode('utf-8')
                    self.sock.sendto(data, address)
                    self.remote = address
                    self.host = True
                    break
        self.state = 'ok'

        self.timeout = time.time()
        self.sock.settimeout(0.5)
        #self.sock.connect(self.remote)
        while self.running:
            try:
                data, address = self.sock.recvfrom(1024)
                data = data.decode('utf-8')
            except:
                if (time.time() - self.timeout)%6 > 5.0:
                    data = 'inf:0:hello!'.encode('utf-8')
                    self.sock.sendto(data, self.remote)
                elif (time.time() - self.timeout)/5 > 2.0:
                    self.state = 'noreply'
                continue

            self.timeout = time.time()
            self.state = 'ok'

            data = data.split(':')
            if data[0] == 'inf':
                if data[2] == 'hello!':
                    self.state = 'ok'
                    data = 'rep:0:hello!'.encode('utf-8')
                    self.sock.sendto(data, self.remote)
                elif data[2] == 'close':
                    self.state = 'close'
                    self.running = False
                else:
                    if data[1] not in self.tmp_id:
                        self.inf_msg[data[1]] = data[2]
                        self.tmp_id[int(data[1])%10] = data[1]
                    else:
                        print('重复消息：', data[0], data[1], data[2])
                    data = 'rep:{}:{}'.format(data[1], data[2])
                    self.sock.sendto(data.encode('utf-8'), self.remote)
            elif data[0] == 'rep':
                print(data[0], data[1], data[2])
                self.rep_msg[data[1]] = data[2]

        self.remote = None
        self.sock.close()
                        
    def send_msg(self, msg):
        #id = str(random.random())
        self.msg_id += 1
        id = str(self.msg_id)
        data = 'inf:{}:{}'.format(id, msg)
        print('-->', data)
        self.sock.sendto(data.encode('utf-8'), self.remote)
        for _ in range(5):
            if id not in self.rep_msg:
                time.sleep(0.1)
                continue
            if self.rep_msg[id] == msg:
                return self.rep_msg.pop(id)
        #重发一次
        print('重发消息：', data)
        self.sock.sendto(data.encode('utf-8'), self.remote)
        for _ in range(5):
            if id not in self.rep_msg:
                time.sleep(0.1)
                continue
            if self.rep_msg[id] == msg:
                return self.rep_msg.pop(id)
        print('重发失败！')
        return None

    def get_msg(self):
        try:
            item = self.inf_msg.popitem()
        except:
            return None
        return item

    def get_stat(self):
        return self.state

    def close(self):
        self.sock.sendto('inf:0:close'.encode('utf-8'), self.remote)
        self.running = False

# 消息框
def msg_box(msg, wnd, f_name=None, f_color=None, f_size=None):
    #创建字体
    if f_name is None:
        f_name = 'STZHONGS.ttf'
    if f_color is None:
        f_color = (0, 0, 0)
    if f_size is None:
        f_size = 18
    font = pygame.font.Font(f_name, f_size)
    msg_img = font.render(msg, True, f_color)
    
    # 创建询问框surface
    msg_rect = msg_img.get_rect()
    box_rect = pygame.Rect(0, 0, msg_rect.w+40, msg_rect.h+40)
    box_surface = pygame.Surface(box_rect.size)
    box_surface.fill((200, 200, 200))

    msg_rect.center = box_rect.center
    # 画2px边框
    box_rect.x = 1
    box_rect.y = 1
    box_rect.w -= 2
    box_rect.h -= 2
    pygame.draw.rect(box_surface, (128, 128, 128), box_rect, 2)

    # 打印信息文本
    box_surface.blit(msg_img, msg_rect)
    box_rect.center = wnd.get_rect().center
    wnd.blit(box_surface, box_rect)
    pygame.display.flip()

# 询问框
def query_box(msg, wnd, f_name=None, f_color=None, f_size=None, yes=' Yes ', no=' No '):
    tmp_surface = wnd.copy()

    #创建字体
    if f_name is None:
        f_name = 'STZHONGS.ttf'
    if f_color is None:
        f_color = (0, 0, 0)
    if f_size is None:
        f_size = 18
    font = pygame.font.Font(f_name, f_size)
    msg_img = font.render(msg, True, f_color)
    yes_img = font.render(yes, True, f_color, (128, 128, 128))
    no_img = font.render(no, True, f_color, (128, 128, 128))
    
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
                wnd.blit(tmp_surface, (0, 0))
                pygame.display.flip()
                return True
            elif no_rect.collidepoint(event.pos):
                wnd.blit(tmp_surface, (0, 0))
                pygame.display.flip()
                return False
        wnd.blit(box_surface, box_rect)
        pygame.display.flip()
        pygame.time.wait(50)










