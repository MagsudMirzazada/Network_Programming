# SCTATCH-UP

import socket
import argparse
import random

MAX_BYTES = 10240

class server:
    def __init__(self):
        self.interface = '127.0.0.1'
        self.port = 65432
    
    def server_(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.interface, self.port))
        print(f'Server is binding to {sock.getsockname()}')
        while True:
            data, addr = sock.recvfrom(MAX_BYTES)
            if random.random() < 0.5:
                print(f'Message dropped from {addr}')
                continue
            text = data.decode('utf-8')
            print(f'{addr} says {text}')

            message = f'[SERVER] Your message arrived'.encode('utf-8')
            sock.sendto(message, addr)


class client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432

    def client_(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        print(f'Client is {sock.getsockname()}')

        delay = 0.1 #seconds
        data = f'It is Message'.encode('utf-8')

        while True:
            sock.send(data)
            print(f'Waiting for delay seconds for a reply')
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES) 
            except socket.timeout:
                delay *= 2
                if delay > 2:
                    raise RuntimeError('Server probably is down')
            else:
                break
        print(f"[Server]'{data.decode('utf-8')}'")
            


def main():
    server1 = server()
    client1 = client()
    
    choices = {'server': server1.server_, 'client': client1.client_}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices, help='Xiarsan sen?')

    args = parser.parse_args()
    func = choices[args.role]
    func()

if __name__ == '__main__':
    main()