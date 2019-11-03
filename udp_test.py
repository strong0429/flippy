import argparse, socket
import time,random

BUFSIZE = 65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.sendto('test!!!'.encode('ascii'), ('<broadcast>', port))
    print('Listening for datagrams at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print('The client at {} says: {!r}'.format(address, text))
        sock.sendto(text.encode('ascii'), address)


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.bind(('', port))
    sock.setblocking(False)
    
    text = 'Broadcast datagram'
    sock.sendto(text.encode('ascii'), ('<broadcast>', port))
    for _ in range(3):
        try:
            time.sleep(random.randint(1, 10)/10)
            data, address = sock.recvfrom(BUFSIZE)
            text = data.decode('ascii')
            print('The server at {} says: {!r}'.format(address, text))
        except BlockingIOError as e:
            print('time out!', e)
            continue
        finally:
            print('finally')

    sock.close()



if __name__ == '__main__':
    '''
    # 查看当前主机名
    print('当前主机名称为 : ' + socket.gethostname())
    
    # 根据主机名称获取当前IP
    print('当前主机的IP为: ' + socket.gethostbyname(socket.gethostname()))
    
    # Mac下上述方法均返回127.0.0.1
    # 通过使用socket中的getaddrinfo中的函数获取真真的IP
    
    # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
    addrs = socket.getaddrinfo(socket.gethostname(),None)
    
    for item in addrs:
        print(item)
        
    # 仅获取当前IPV4地址
    print('当前主机IPV4地址为:' + [item[4][0] for item in addrs if ':' not in item[4][0]][0])

    # 同上仅获取当前IPV4地址
    for item in addrs:
        if ':' not in item[4][0]:
            print('当前主机IPV4地址为:' + item[4][0])
            break
    '''

    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at; network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
    
